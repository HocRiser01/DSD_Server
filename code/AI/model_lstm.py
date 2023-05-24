from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, SubsetRandomSampler
import torch.nn.functional as F

class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        # self.soft = nn.softmax(dim=2)

    def forward(self, x):
        # print(x.shape)
        # exit(0)
        lstm_out, _ = self.lstm(x)

        # print(lstm_out.shape)
        # print(_.shape)
        out = self.fc(lstm_out)
        # out2 =F.softmax(out,dim=-1)
        return out


class FHBDataset(Dataset):
    def __init__(self, Data, Label):
        self.data = Data
        self.label = Label
        self.data_len = len(Label)
        # print(self.data_len)
        print("data load finish")

    def __getitem__(self, index):
        single_label = self.label[index]
        return (self.data[index], single_label)

    def __len__(self):
        return self.data_len

BATCH_SIZE = 32
EPOCH = 100


def Train(X_train,X_test,y_train,y_test):
    X_train = X_train.reshape(-1, 54)
    X_test = X_test.reshape(-1, 54)
    y_test = y_test.reshape(-1)
    y_train = y_train.reshape(-1)
    cuda_gpu = torch.cuda.is_available()
    lstm = LSTM(54,105,7).float()
    if (cuda_gpu):
        lstm = torch.nn.DataParallel(lstm, device_ids=[0]).cuda()
    optimizer = torch.optim.Adam(lstm.parameters(), lr=0.001)
    Traindata = FHBDataset(X_train,y_train)
    Testdata  = FHBDataset(X_test, y_test)
    train_loader = DataLoader(Traindata, batch_size=BATCH_SIZE,shuffle=True)
    test_loader  = DataLoader(Testdata, batch_size=BATCH_SIZE)
    acc = 0
    for epoch in range(EPOCH):
        for step, (b_x, b_y) in enumerate(train_loader):
            if (cuda_gpu):
                b_x = b_x.cuda()
                b_y = b_y.cuda()
            output = lstm(b_x.float())
            # output = output.reshape(output.shape[0],output.shape[2])
            loss = F.cross_entropy(output.float(), b_y.long())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        corrects = 0
        for _, (b_x, b_y) in enumerate(test_loader):
            if (cuda_gpu):
                b_x = b_x.cuda()
                b_y = b_y.cuda()
            output = lstm(b_x.float())
            corrects += (torch.max(output, 1)
                        [1].view(b_y.size()).data == b_y.data).sum()
        size = len(Testdata)
        accuracy = 100.0 * corrects / size
        acc = accuracy
        print('Epoch: {:2d}Evaluation - acc: {:3.4f}'.format(epoch,acc))
    return (lstm,acc)


def predict_proba(model,data):
    Data = torch.Tensor(data)
    Data = Data.reshape(1,Data.shape[0])
    output = model(Data)
    return F.softmax(output,dim=-1).clone().cpu().detach().numpy()


def predict(model,data):
    Data = torch.Tensor(data)
    Data = Data.reshape(1, Data.shape[0])
    output = model(Data)
    return F.softmax(output, dim=-1).max()[1]


def get_sorce(model,X,y):
    X = X.reshape(-1, 54)
    y = y.reshape(-1)
    Testdata = FHBDataset(X, y)
    test_loader = DataLoader(Testdata, batch_size=BATCH_SIZE)
    corrects = 0
    for _, (b_x, b_y) in enumerate(test_loader):
        output = model(b_x.float())
        output = output.reshape(output.shape[0], output.shape[2])
        corrects += (torch.max(output, 1)
                     [1].view(b_y.size()).data == b_y.data).sum()
    size = len(Testdata)
    accuracy = 100.0 * corrects / size
    return accuracy


if __name__ == '__main__':
    old_data = pickle.load(open("./data/data.pth", "rb"))
    X = old_data[:, :, :54]
    Y = old_data[:, :, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    (Model, _) = Train(X_train, X_test, y_train, y_test)
    pickle.dump(Model, open("./model_lib/base/{}.pth".format('lstm'), 'wb'))
    print(_)
