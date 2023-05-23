import os
from model_SVM import *
import pickle
import numpy as np

gen = 'SVM'
#[KNN,SVM,lstm]
record=["down","left","right","sit","stand","up","walk"]

base_proba = 0.25
def check(data,model):
    for frame in data:
        P = predict_proba(model,frame[:54])
        # print(int(frame[55]))
        # print(P.shape)
        if (P[0][int(frame[55])] < base_proba): return 0
    return 1

def check2(data,model):
    for frame in data:
        P = predict_proba(model,frame[:54])
        if (P.max() < base_proba ): return 0
    return 1

def get_predict_inter(data,model):
    rP = np.zeros((1,7),dtype=float)
    for frame in data:
        P = predict_proba(model,frame[:54])
        # print(P.shape)
        rP=rP+P
    return rP.argmax()

from sklearn.model_selection import train_test_split

def model_train(new_data):
    X=new_data[ :, : , :54]
    Y=new_data[ :, : , -1]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4)
    old_data = pickle.load(open("./data/data.pth",'rb'))
    X_train = X_train.tolist()
    y_train = y_train.tolist()
    X_train = [x for x in X_train for i in range(2)]
    y_train = [x for x in y_train for i in range(2)]
    for data in old_data:
        X_train.append(data[:, :54].tolist())
        y_train.append(data[:,  -1].tolist())

    X_train = np.array(X_train)
    y_train = np.array(y_train)
    (model,acc) = Train(X_train,X_test,y_train,y_test)
    return model,acc


def get_train(uid,train_data_set):
    model=pickle.load(open("./model_lib/base/{}.pth".format(gen),'rb'))
    R = get_progress(uid,train_data_set)
    if (R.min()<1.0): return -2
    newdataset = []
    data_set = train_data_set
    for data in data_set:
        if (check(data,model)): newdataset.append(data)
    newdataset=np.array(newdataset)
    # data_clear(train_data_set,model)
    try:
        (Umodel,acc)=model_train(newdataset)
    except Exception as e:
        raise e
    clear(uid)
    pickle.dump(Umodel,open("./model_lib/usr/{}.pth".format(uid),'wb'))
    return acc

def get_predict(uid,flow,opt=-1):
    # print("flow:",flow)
    if (opt==1):
        f=open("./model_lib/base/{}.pth".format(gen),"rb")
    elif (opt==0):
        Path="./model_lib/usr/{}.pth".format(uid)
        if (os.path.exists(Path)):
            f=open(Path,"rb")
        else:
            return -1
    elif (opt==-1):
        Path = "./model_lib/usr/{}.pth".format(uid)
        if (os.path.exists(Path)):
            f = open(Path,'rb')
        else:
            f = open("./model_lib/base/{}.pth".format(gen),"rb")
    model=pickle.load(f)
    model2=pickle.load(open("./model_lib/base/{}.pth".format(gen),"rb"))
    flow2 = flow
    # print("flow2:",flow2.shape)
    # pred = get_predict_inter(flow2, model)
    # return pred
    if (check2(flow2,model2)):
        pred = get_predict_inter(flow2,model)
        return pred
    else:
        return -2


def clear(uid):
    Path = "./model_lib/usr/{}.pth".format(uid)
    if (os.path.exists(Path)):
        os.remove(Path)
    return

def get_train_time(train_data_set):
    return 100*train_data_set.shape[0]

base_accept = 900

def get_progress(uid,train_data_set):
    model = pickle.load(open("./model_lib/base/{}.pth".format(gen),"rb"))
    data_set=train_data_set
    result = np.zeros((7),dtype=float)
    for data in data_set:
        if (check(data,model)):
            for frame in data:
                result[int(frame[55])]=result[int(frame[55])]+1
    return result/base_accept

def get_state(uid):
    Path = "./model_lib/usr/{}.pth".format(uid)
    if (os.path.exists(Path)):
        return 1
    else:
        return 0
