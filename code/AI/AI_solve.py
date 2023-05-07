import onnxruntime as ort
import torch
import numpy as np
import os
import main


def data_clear(train_data,dataset):


def check(data_input):
    return 1


def AI_clear(uid):
    path="./Model/"+uid+".pt"
    if os.path.exists(path):
        os.remove(path)


def AI_get_predict(uid,predict_list,opt):
    if (check(predict_list)==0): return -2
    if (opt==0):
        path = "./Spec_Model/" + uid + ".pt"
    else:
        path = "./Norm_Model/base.pt"
    try:
        model = torch.load(path)
        predict = model(predict_list)
    except:
        return -1;
    return predict


def AI_get_train(uid,train_file):
    AI_clear(uid)
    train=split(train_file)
    main(0,train_file)
    return 0

