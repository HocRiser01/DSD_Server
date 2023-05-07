import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import random
import math

torch.manual_seed(2023)
torch.cuda.manual_seed_all(2023)
np.random.seed(2023)
random.seed(2023)
torch.backends.cudnn.deterministic = True


class deep_packet(nn.Module):
    # Deep packet: a novel approach for encrypted traffic classification using deep learning

    def __init__(self):
        super(deep_packet, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=200, kernel_size=5, stride=2, padding=2),
            nn.BatchNorm1d(200),
            nn.ReLU(),
        )
        self.conv2 = nn.Sequential(
            nn.Conv1d(in_channels=200, out_channels=200, kernel_size=4, stride=2, padding=2),
            nn.BatchNorm1d(200),
            nn.ReLU(),
        )
        self.fc1 = nn.Sequential(
            nn.Linear(in_features=200, out_features=100),
            nn.Dropout(p=0.05),
            nn.ReLU(),
        )
        self.fc2 = nn.Sequential(
            nn.Linear(in_features=100, out_features=50),
            nn.Dropout(p=0.05),
            nn.ReLU(),
        )
        self.fc3 = nn.Sequential(
            nn.Linear(in_features=50, out_features=6),
            nn.Dropout(p=0.05),
        )
        self.pooling = nn.AdaptiveAvgPool1d(1)

    def forward(self, x):
        x = x.reshape(-1, 1, 50).float()
        out = self.conv1(x)
        out = self.conv2(out)
        # out = out.transpose(-2, -1)
        out = self.pooling(out)
        out = out.view(out.size(0), -1)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.fc3(out)

        if not self.training:
            return F.softmax(out, dim=-1).max(1)[1]
        return out


class FS_net(nn.Module):
    # FS-Net: A Flow Sequence Network For Encrypted Traffic Classification
    def __init__(self):
        super(FS_net, self).__init__()
        self.embedding = nn.Embedding(num_embeddings=300, embedding_dim=128)

        self.lstm1 = nn.Sequential(
            nn.LSTM(128, 128, batch_first=True, bidirectional=True),
        )
        self.lstm2 = nn.Sequential(
            nn.LSTM(256, 128, batch_first=True, bidirectional=True),
        )
        self.lstm3 = nn.Sequential(
            nn.LSTM(512, 128, batch_first=True, bidirectional=True),
        )
        self.lstm4 = nn.Sequential(
            nn.LSTM(256, 128, batch_first=True, bidirectional=True),
        )
        self.fc1 = nn.Sequential(
            nn.Linear(in_features=512, out_features=64),
            nn.ReLU()
        )
        self.fc2 = nn.Sequential(
            nn.Linear(in_features=64, out_features=6)
        )
        self.pooling = nn.AdaptiveAvgPool1d(1)

    def forward(self, x):
        x = self.embedding(x)
        h1, _ = self.lstm1(x)
        h2, _ = self.lstm2(h1)
        h3 = torch.cat([h1, h2], 2)

        h4, _ = self.lstm3(h3)
        h5, _ = self.lstm4(h4)
        out = torch.cat([h4, h5], 2)

        out = out.transpose(-2, -1)
        out = self.pooling(out)
        out = out.view(out.size(0), -1)
        out = self.fc1(out)
        out = self.fc2(out)

        if not self.training:
            return F.softmax(out, dim=-1).max(1)[1]
        return out


class lstm_attention(nn.Module):
    # Attention-based bidirectional GRU networks for efficient HTTPS traffic classification
    def __init__(self):
        super(lstm_attention, self).__init__()
        self.embedding = nn.Embedding(num_embeddings=300, embedding_dim=128)

        self.lstm1 = nn.LSTM(128, 128, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(256, 128, batch_first=True, bidirectional=True)

        self.query = nn.Parameter(torch.Tensor(256, 1))

        self.fc1 = nn.Sequential(
            nn.Linear(in_features=256, out_features=256),
            nn.ReLU()
        )

        self.fc2 = nn.Linear(in_features=256, out_features=6)

    def forward(self, x):
        out = self.embedding(x)
        out, _ = self.lstm1(out)
        out, _ = self.lstm2(out)

        key = self.fc1(out)  # [50, 256], [256, 1] 50 * 256 * 256
        attention_weight = torch.matmul(key, self.query)
        attention_weight = F.softmax(attention_weight, dim=1)

        out = out * attention_weight
        out = torch.sum(out, dim=1)
        out = self.fc2(out)

        if not self.training:
            return F.softmax(out, dim=-1).max(1)[1]
        return out


class APP_net(nn.Module):
    # App-Net: A Hybrid Neural Network for Encrypted Mobile Traffic Classification
    def __init__(self):
        super(APP_net, self).__init__()
        self.embedding = nn.Embedding(num_embeddings=300, embedding_dim=128)

        self.lstm1 = nn.LSTM(128, 128, batch_first=True, bidirectional=True)
        self.lstm2 = nn.LSTM(256, 128, batch_first=True, bidirectional=True)

        self.conv1 = nn.Sequential(
            nn.Conv1d(in_channels=128, out_channels=256, kernel_size=5, stride=1, padding=2),
            nn.MaxPool1d(kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(256)
        )

        self.conv2 = nn.Sequential(
            nn.Conv1d(in_channels=256, out_channels=256, kernel_size=5, stride=1, padding=2),
            nn.MaxPool1d(kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(256)
        )

        self.pooling = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(in_features=256, out_features=6)

    def forward(self, x):
        h = self.embedding(x)
        h1, _ = self.lstm1(h)
        h1, _ = self.lstm2(h1)
        h1 = h1.transpose(-2, -1)
        h1 = self.pooling(h1).view(h1.size(0), -1)

        h2 = h.transpose(-2, -1)
        h2 = self.conv1(h2)
        h2 = self.conv2(h2)
        h2 = self.pooling(h2).view(h2.size(0), -1)

        out = h1 + h2
        out = self.fc(out)

        if not self.training:
            return F.softmax(out, dim=-1).max(1)[1]
        return out


class DNN(nn.Module):
    # A deep learning method with wrapper based feature extraction for wireless intrusion detection system

    def __init__(self):
        super(DNN, self).__init__()
        # input is N C H W
        self.num_class = 6
        self.conv2_filters = 100
        self.embedding = nn.Embedding(num_embeddings=300, embedding_dim=100)
        self.fc1 = nn.Sequential(
            nn.Linear(self.conv2_filters, out_features=100),
            nn.ReLU()
        )
        self.fc2 = nn.Sequential(
            nn.Linear(100, out_features=100),
            nn.ReLU()
        )
        self.fc3 = nn.Sequential(
            nn.Linear(100, out_features=100),
            nn.ReLU()
        )
        self.fc4 = nn.Sequential(
            nn.Linear(in_features=100, out_features=1),
            nn.ReLU()
        )
        self.fc5 = nn.Sequential(
            nn.Linear(in_features=50, out_features=6),
            # nn.ReLU()
        )

    def forward(self, x):
        # x: B 1 H W
        # flatten
        # out = x.view(x.shape[0], -1, self.conv2_filters)
        out = self.embedding(x)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.fc3(out)
        out = self.fc4(out)
        out = out.view(out.shape[0], -1)
        out = self.fc5(out)

        if not self.training:
            return F.softmax(out, dim=-1).max(1)[1]
        return out


class RNN(nn.Module):
    # Novel Deep Learning-Enabled LSTM Autoencoder Architecture for Discovering Anomalous Events From Intelligent Transportation Systems

    def __init__(self):
        super(RNN, self).__init__()
        # input is N C H W
        self.embedding = nn.Embedding(num_embeddings=300, embedding_dim=128)
        self.lstm1 = nn.Sequential(
            nn.LSTM(128, 128, batch_first=True),
        )
        self.lstm2 = nn.Sequential(
            nn.LSTM(128, 64, batch_first=True),
        )
        self.lstm3 = nn.Sequential(
            nn.LSTM(64, 32, batch_first=True),
        )
        self.fc = nn.Sequential(
            nn.Linear(in_features=32, out_features=6),
            # nn.ReLU()
        )
        self.pooling = nn.AdaptiveAvgPool1d(1)

    def forward(self, x):
        # x: B 1 H W
        # flatten
        out = self.embedding(x)
        out, _ = self.lstm1(out)
        out, _ = self.lstm2(out)
        out, _ = self.lstm3(out)
        out = out.transpose(-2, -1)
        out = self.pooling(out).view(out.size(0), -1)
        out = self.fc(out)

        if not self.training:
            return F.softmax(out, dim=-1).max(1)[1]
        return out


class LuNet(nn.Module):
    # LuNet: A Deep Neural Network for Network Intrusion Detection

    def __init__(self):
        super(LuNet, self).__init__()
        self.embedding = nn.Embedding(num_embeddings=300, embedding_dim=64)
        self.conv1 = nn.Sequential(
            nn.Conv1d(in_channels=64, out_channels=32, kernel_size=5,
                      stride=1, padding=2),
            nn.MaxPool1d(kernel_size=2, stride=1),
            nn.BatchNorm1d(32)
        )
        self.lstm1 = nn.Sequential(
            nn.LSTM(32, 100, batch_first=True),
        )

        self.fc1 = nn.Sequential(
            nn.Linear(in_features=100, out_features=6),
            # nn.ReLU()
        )

    def forward(self, x):
        # x: B 1 H W
        # flatten
        out = self.embedding(x)
        out = out.transpose(-2, -1)
        out = self.conv1(out)
        out = out.transpose(-2, -1)
        out, _ = self.lstm1(out)
        # only use the last state in LSTM
        out = out.mean([1])
        out = self.fc1(out)

        if not self.training:
            return F.softmax(out, dim=-1).max(1)[1]
        return out