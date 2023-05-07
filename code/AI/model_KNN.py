from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle
import numpy as np

def predict_proba(model,data):
    data = data.reshape(1,-1)
    return model.predict_proba(data)

def predict(model,data):
    return model.predict(data)

def get_sorce(model,X,y):
    X=X.reshape(-1,54)
    y=y.reshape(-1)
    pred = predict(model,X)
    acc = np.sum(pred.equal(y))
    return 1.0*acc/y.shape[0]

def Train(X_train,X_test,y_train,y_test):
    X_train =X_train.reshape(-1,54)
    X_test  =X_test.reshape(-1,54)
    y_test =y_test.reshape(-1)
    y_train=y_train.reshape(-1)
    KNN = KNeighborsClassifier(n_neighbors=6, p=2.5)
    KNN.fit(X_train,y_train)
    acc = KNN.score(X_test,y_test)
    return (KNN,acc)

if __name__ == '__main__':
    old_data = pickle.load(open("./data/data.pth","rb"))
    X = old_data[: , :, :54]
    Y = old_data[:, :,-1]
    for T in Y:
        print(T)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    (Model,_) = Train(X_train, X_test, y_train, y_test)
    pickle.dump(Model, open("./model_lib/base/{}.pth".format('KNN'),'wb'))
    # print(Model.n_classes)
    print(_)
