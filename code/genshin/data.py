from . import network
from . import motion

import sys
sys.path.append("..")
import dbest as db
import AI as ai

import threading
import http

__dataCollectionThread: dict
__dataCollectionFlag: dict

def getData(jsonData: dict):
    tp = "GetDataResponse"

    id = jsonData.get("id")

    try:
        return db.GetMotionData(account)
    except Exception as e:
        return network.message(tp, str(e))

    return message(tp, "GetDataSucceed")


def discardData(jsonData: dict):
    tp = "DiscardDataResponse"

    id = jsonData.get("id")
    startTime = jsonData.get("startTime")

    try:
        db.DeleteMotionRecord(id, startTime)
    except Exception as e:
        return network.message(tp, str(e))

    return network.message(tp, "DiscardDataSucceed")

def changeLabel(jsonData: dict):
    tp = "ChangeLabelResponse"

    account = jsonData.get("account")
    startTime = jsonData.get("startTime")
    label = jsonData.get("label")

    try:
        db.ModifyMotionRecord(account, startTime, label)
    except Exception as e:
        returnnetwork.message(tp, str(e))

    return network.message(tp, "ChangeLabelSucceed")

def collectData(jsonData: dict):
    tp = "CollectDataResponse"

    userID = jsonData.get("userID")
    label = jsonData.get("label")

    try:
        ip, port = db.GetDeviceInfo(userID)
    except Exception as e:
        return network.message(tp, str(e))

    mutex = threading.Lock()
    mutex.acquire()

    if __dataCollectionThread.get(userID) != None:
        __dataCollectionFlag[userID] = False
        while __dataCollectionThread.get(userID).is_alive() == True:
            continue

    __dataCollectionThread[userID] = threading.Thread(
        target=__collect, args=(userID, label, ip, port))
    __dataCollectionFlag[userID] = True

    mutex.release()

    return message(tp, "CollectDataSucceed")

def collectDataStop(jsonData: dict):
    tp = "CollectDataStopResponse"

    userID = jsonData.get("userID")

    if __dataCollectionThread.get(userID) == None:
        return network.message(tp, "collection hasn't started")

    mutex = threading.Lock()
    mutex.acquire()

    __dataCollectionFlag[userID] = False
    while __dataCollectionThread.get(userID).is_alive() == True:
        continue

    __dataCollectionThread.pop(userID)
    __dataCollectionFlag.pop(userID)

    mutex.release()

    return message(tp, "CollectDataStopSucceed")

def getPrediction(jsonData: dict):
    tp = "GetPredictionResponse"

    userID = jsonData.get("userID")

    try:
        motionData = db.GetMotionData(userID)
    except Exception as e:
        return str(e)

    try:
        ip, port = db.GetDeviceInfo(userID)
    except Exception as e:
        return network.message(tp, str(e))

    conn = http.client.HTTPConnection("%s:%d" % (ip, port))
    request = json.dump({"type": "GetRealtimeData"})
    headers = {
        "Content-Type": "application/json"
    }

    try:
        conn.request("POST", "/", request, headers)
        response = conn.getresponse()
        body = response.read().decode()
        jsonData = json.loads(body)
    except Exception as e:
        network.message(tp, str(e))

    result = ai.get_predict(parseMotion(jsonData))

    if result == -2:
        return network.message(tp, "PredictionDataInvalid")
    elif result == -1:
        return network.message(tp, "PredictionModelMissing")
    else:
        return network.message(tp, motion.label[result])

def resetModel(jsonData: dict):
    tp = "ResetModelRespose"

    userID=jsonData.get("userID")

    ai.clear(userID)

    return message(tp, "ResetModelSucceed")

def __collect(userID: str, label: int, ip: str, port: int):
    data = np.array([])
    frame = np.full((5, 55), 0)
    count = 0

    conn = http.client.HTTPConnection("%s:%d" % (ip, port))
    request = json.dump({"type": "GetRealtimeData"})
    headers = {
        "Content-Type": "application/json"
    }

    while __dataCollectionFlag[userID] == True:
        try:
            conn.request("POST", "/", request, headers)
            response = conn.getresponse()
            body = response.read().decode()
            jsonData = json.loads(body)
        except:
            continue

        frame[count] = motion.parseMotion(jsonData)
        count += 1

        if count == 5:
            data = np.append(data, frame.reshape(1, 5, 55))
            count = 0

        sleep(200)

    try:
        db.SaveMotionData(userID, time.time(), label, data)
    except:
        return