import pickle
import os
import warnings
from interfaces import *

warnings.filterwarnings("ignore")
clear("a")
old_data = pickle.load(open("./data/data.pth","rb"))
X = old_data[: , :, :54]
Y = old_data[:, :,-1]
uid='123'
clear(uid)
# print(get_state(uid))
print("predict: ", get_predict(uid,X[0]))
print("Y[0]: ",Y[0])
# print(get_train_time(old_data))
print("progress: ",get_progress(uid,old_data))
print("train: ",get_train(uid,old_data))
print("state: ",get_state(uid))
print("predict: ",get_predict(uid,X[0]))
print("Y[0]: ",Y[0])
# print(get_predict("a",))