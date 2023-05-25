import motion
import network
import log

import dbest as db
import AI as ai

import threading
import time
import http
import http.client
import json

dataCollectionThread = {}
dataCollectionFlag = {}
dataCollectionMutex = threading.Lock()


def getData(jsonData: dict):
    tp = "GetDataResponse"

    id = jsonData.get("id")

    log.log("Try to get data [id: %s]." % (id))

    try:
        labels, createTime, lastTime = db.Database().GetMotionRecord(id)
        motionArray = []
        recordLen = len(labels)

        for i in range(recordLen):
            motionRecord = {
                "typeOfMotion": labels[i],
                "start time": createTime[i],
                "duration": lastTime[i]
            }

            motionArray.append(motionRecord)

        return motionArray

    except Exception as e:
        log.log("Failed to get data [error: %s]" % (str(e)))
        return network.message(tp, str(e))


def discardData(jsonData: dict):
    tp = "DiscardDataResponse"

    id = jsonData.get("id")
    startTime = jsonData.get("startTime")

    log.log("Try to discard data [id: %s, startTime: %s]" % (
        id, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime))))

    try:
        db.Database().DeleteMotionRecord(id, startTime)
    except Exception as e:
        log.log("Failed to discard data [error: %s]" % str(e))
        return network.message(tp, str(e))

    return network.message(tp, "DiscardDataSucceed")


def changeLabel(jsonData: dict):
    tp = "ChangeLabelResponse"

    id = jsonData.get("id")
    startTime = jsonData.get("startTime")
    label = jsonData.get("label")

    log.log("Try to change label [id: %s, startTime: %s, label: %s]" % (
        id, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(startTime)), motion.label[label]))

    try:
        db.Database().ModifyMotionRecord(id, startTime, label)
    except Exception as e:
        log.log("Failed to change label [error: %s]" % (str(e)))
        return network.message(tp, str(e))

    return network.message(tp, "ChangeLabelSucceed")


def collectData(jsonData: dict):
    tp = "CollectDataResponse"

    id = jsonData.get("id")
    label = jsonData.get("label")

    log.log("Try to start data collection [id: %s, label: %s]" % (
            id, motion.label[label]))

    try:
        ip, port = db.Database().GetDeviceInfo(id)
        log.log("[ip: %s, port: %s]" % (ip, port))
    except Exception as e:
        log.log("Failed to start data collection [error: %s]" % str(e))
        return network.message(tp, str(e))

    dataCollectionMutex.acquire()

    if dataCollectionThread.get(id) != None:
        dataCollectionFlag[id] = False
        while dataCollectionThread.get(id).is_alive() == True:
            continue

    dataCollectionThread[id] = threading.Thread(
        target=collect, args=(id, label, ip, port))
    dataCollectionFlag[id] = True

    dataCollectionMutex.release()

    dataCollectionThread[id].start()

    return network.message(tp, "CollectDataStarted")


def collect(id: str, label: int, ip: str, port: int):
    data = []

    jsonRequest = json.dumps({"type": "GetRealtimeData"})
    headers = {
        "Content-Type": "application/json"
    }

    while dataCollectionFlag[id] == True:
        conn = http.client.HTTPConnection("%s:%s" % (ip, port))

        try:
            conn.request("POST", "/", jsonRequest, headers)
            response = conn.getresponse()
            body = response.read().decode()
            jsonData = json.loads(body)
        except Exception as e:
            log.log(
                "Get error from device [error: %s]. Continue collection." % (str(e)))
            continue

        if jsonData.get("type") == "GetRealtimeDataResponse":
            data.append(jsonData)

        time.sleep(0.2)

    try:
        db.Database().SaveMotionData(id, time.time(), label, data)
    except Exception as e:
        log.log("Failed to save motion data [error: %s]" % (str(e)))
        return


def collectDataStop(jsonData: dict):
    tp = "CollectDataStopResponse"

    id = jsonData.get("id")

    log.log("Try to stop collection [id: %s]" % (id))

    if dataCollectionThread.get(id) == None:
        log.log("Failed to stop collection [error: CollectionNotStarted]")
        return network.message(tp, "CollectionNotStarted")

    # some error may cause the collection thread to be terminated
    if dataCollectionThread[id].is_alive() == False:
        log.log(
            "Failed to stop collection [error: CollectionUnexpectedlyTerminated]")
        return network.message(tp, "CollectionUnexpectedlyTerminated")

    dataCollectionMutex.acquire()

    dataCollectionFlag[id] = False
    while dataCollectionThread[id].is_alive() == True:
        continue

    dataCollectionThread.pop(id)
    dataCollectionFlag.pop(id)

    dataCollectionMutex.release()

    return network.message(tp, "CollectDataStopped")


def getPrediction(jsonData: dict):
    tp = "GetPredictionResponse"

    id = jsonData.get("id")

    log.log("Try to get prediction [id: %s]" % (id))

    try:
        ip, port = db.Database().GetDeviceInfo(id)
    except Exception as e:
        log.log("Failed to get prediction [error: %s]" % (str(e)))
        return network.message(tp, str(e))

    conn = http.client.HTTPConnection("%s:%d" % (ip, port))
    request = json.dumps({"type": "GetRealtimeData"})
    headers = {
        "Content-Type": "application/json"
    }

    try:
        conn.request("POST", "/", request, headers)
        response = conn.getresponse()
        body = response.read().decode()
        jsonData = json.loads(body)
    except Exception as e:
        log.log("Failed to get prediction [error: %s]" % (str(e)))
        return network.message(tp, str(e))

    if jsonData.get("type") == "GetRealtimeDataResponse":
        result = ai.get_predict(motion.parseMotion(jsonData))
    else:
        return network.message(tp, "PredtionNetworkError")

    if result == -2:
        return network.message(tp, "PredictionDataInvalid")
    elif result == -1:
        return network.message(tp, "PredictionModelMissing")
    else:
        return network.message(tp, motion.label[result])


def resetModel(jsonData: dict):
    tp = "ResetModelRespose"

    id = jsonData.get("id")

    log.log("Try to reset model [id: %s]" % (id))

    ai.clear(id)

    return network.message(tp, "ResetModelSucceed")
