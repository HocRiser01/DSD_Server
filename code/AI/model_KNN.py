from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import pickle
import numpy as np

RECOPOINTS_NUM=5
ROUND_NUM =500
FEAT_NUM =54

def dist(a,b,c):
    Dist=0.0
    num = a.shape[0]
    for i in range(num):
        Dist =Dist + c[i] *abs(a[i] - b[i])
    return Dist

def alg_recommend2(feat, featclasses, featlen, weight):
    distlist = np.zeros(featlen)
    recogoodlist = np.zeros(RECOPOINTS_NUM, dtype=int)
    recobadlist = np.zeros(RECOPOINTS_NUM, dtype=int)

    for i in range(ROUND_NUM):
        id = i % featlen
        print("\rLearning weights... %d (%d-%d)" % (i, 0, ROUND_NUM), end="")
        trueclass = featclasses[id]
        for k in range(featlen):
            distlist[k] = dist(feat[id], feat[k], weight)
        # set my own distance to max
        max_dist = np.amax(distlist)
        distlist[id] = max_dist

        point_badness = 0
        max_good_dist = 0 # the greatest distance of all the good neighbours NEIGHBOUR_NUM
        # find the good neighbors: NEIGHBOUR_NUM lowest distlist values of the same class
        for k in range(RECOPOINTS_NUM):
            min_ind = np.argmin(distlist[featclasses == trueclass])
            min_dist = distlist[min_ind]
            if min_dist > max_good_dist:
                max_good_dist = min_dist
            distlist[min_ind] = max_dist
            recogoodlist[k] = min_ind

        distlist[featclasses == trueclass] = max_dist
        for k in range(RECOPOINTS_NUM):
            ind = np.argmin(distlist)
            if distlist[ind] <= max_good_dist:
                point_badness += 1
            distlist[ind] = max_dist
            recobadlist[k] = ind

        point_badness /= RECOPOINTS_NUM
        point_badness += 0.2

        featdist = np.zeros(FEAT_NUM)
        badlist = np.zeros(FEAT_NUM, dtype=int)
        min_badlist = 0
        count_badlist = 0
        for f in range(FEAT_NUM):
            if weight[f] == 0:
                badlist[f] = 0
            else:
                max_good = 0.0
                count_bad = 0
                for k in range(RECOPOINTS_NUM):
                    n = abs(feat[id][f] - feat[recogoodlist[k]][f])
                    if feat[id][f] == -1 or feat[recogoodlist[k]][f] == -1:
                        n = 0
                    if n >= max_good:
                        max_good = n
                for k in range(RECOPOINTS_NUM):
                    n = abs(feat[id][f] - feat[recobadlist[k]][f])
                    if feat[id][f] == -1 or feat[recobadlist[k]][f] == -1:
                        n = 0
                    featdist[f] += n
                    if n <= max_good:
                        count_bad += 1
                badlist[f] = count_bad
                if count_bad < min_badlist:
                    min_badlist = count_bad

        for f in range(FEAT_NUM):
            if badlist[f] != min_badlist:
                count_badlist += 1

        w0id = []
        change = []
        temp = 0
        C1 = 0
        C2 = 0
        for f in range(FEAT_NUM):
            if badlist[f] != min_badlist:
                w0id.append(f)
                change.append(weight[f] * 0.02 * badlist[f] / RECOPOINTS_NUM)
                C1 += change[temp] * featdist[f]
                C2 += change[temp]
                weight[f] -= change[temp]
                temp += 1

        total_fd = 0
        for f in range(FEAT_NUM):
            if badlist[f] == min_badlist and weight[f] > 0:
                total_fd += featdist[f]

        for f in range(FEAT_NUM):
            if badlist[f] == min_badlist and weight[f] > 0:
                weight[f] += C1 / total_fd
    # print(weight)
    return weight


from sklearn.base import ClassifierMixin


class KNN_(KNeighborsClassifier):
    def __init__(self):
        super().__init__(n_neighbors=5, metric='manhattan')
        self.wight = np.random.rand(54)
    def fit(self,X_train,y_train):
        print(len(y_train))
        self.wight=alg_recommend2(X_train,y_train,len(y_train),self.wight)
        print(self.wight)
        nX_train = X_train.copy()
        for line in nX_train:
            for i in range(54):
                line[i] = line[i] * self.wight[i]
        return super().fit(nX_train,y_train)
    def predict_proba(self,data):
        data2 = data.copy()#np.zeros(data.shape[0], 54)
        for line in data2:
            for i in range(54):
                line[i] = line[i] * self.wight[i]
        return super().predict_proba(data2)

    def predict(self,data):
        data2 = data.copy()#np.zeros(data.shape[0],54)
        for line in data2:
            for i in range(54):
                line[i] = line[i]*self.wight[i]
        return super().predict(data2)

    def score(self,X_test,y_test,sample_weight=None):
        nX_test = X_test.copy()
        for line in nX_test:
            for i in range(54):
                line[i] = line[i]*self.wight[i]
        y_pred=super().predict(nX_test)
        print(classification_report(y_test, y_pred))
        from sklearn.metrics import accuracy_score
        return accuracy_score(y_test, self.predict(X_test))

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

from sklearn.metrics import classification_report
def Train(X_train,X_test,y_train,y_test):
    X_train =X_train.reshape(-1,54)
    X_test  =X_test.reshape(-1,54)
    y_test =y_test.reshape(-1)
    y_train=y_train.reshape(-1)
    KNN = KNN_()
    KNN.fit(X_train,y_train)
    # print(X_test)
    acc = KNN.score(X_test,y_test)
    # print(X_test)
    print(classification_report(y_test, KNN.predict(X_test)))
    # print(X_test)
    return (KNN,acc)

if __name__ == '__main__':
    old_data = pickle.load(open("./data/data.pth","rb"))
    X = old_data[: , :, :54]
    Y = old_data[:, :,-1]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)
    (Model,_) = Train(X_train, X_test, y_train, y_test)
    pickle.dump(Model, open("./model_lib/base/{}.pth".format('KNN'),'wb'))
    print(_)
