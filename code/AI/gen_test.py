import pickle
import os
from interfaces import *
clear("a")
old_data = pickle.load(open("./data/data.pth","rb"))
X = old_data[: , :, :54]
Y = old_data[:, :,-1]
uid='123'
clear(uid)
# print(get_state(uid))
print(get_predict(uid,X[0]))
print(Y[0])
# print(get_train_time(old_data))
print(get_progress(uid,old_data))
print(get_train(uid,old_data))
print(get_state(uid))
print(get_predict(uid,X[0]))
print(Y[0])
# print(get_predict("a",))