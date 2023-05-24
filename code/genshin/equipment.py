import network
import log

import dbest as db
import AI as ai

import http
import json


def connectEquipment(jsonData: dict):
    tp = "ConnectEquipmentResponse"

    id = jsonData.get("id")
    ip = jsonData.get("ip")
    port = jsonData.get("port")

    log.log("Try to bind device [id: %s, ip: %s, port: %d]." % (id, ip, port))

    try:
        db.Database().BindDevice(id, ip, port)
    except Exception as e:
        log.log("Failed to bind device [error: %s]." % (str(e)))
        return network.message(tp, str(e))

    return network.message(tp, "ConnectEquipmentSucceed")


def disconnectEquipment(jsonData: dict):
    tp = "DisconnectEquipmentResponse"

    id = jsonData.get("id")

    log.log("Try to unbind device [id: %s]." % (id))

    try:
        db.Database().UnbindDevice(id)
    except Exception as e:
        log.log("Failed to unbind device [error: %s]" % (str(e)))
        return network.message(tp, str(e))

    return network.message(tp, "DisconnectEquipmentResponse")


def getSensorDetails(jsonData: dict):
    tp = "GetSensorDetailsResponse"

    id = jsonData.get("id")

    log.log("Try to get sensor details [id: %s]" % (id))

    try:
        ip, port = db.Database().GetDeviceInfo(id)
    except Exception as e:
        log.log("Failed to get sensor details [error: %s]" % (str(e)))
        return network.message(tp, str(e))

    conn = http.client.HTTPConnection("%s:%d" % (ip, port))
    request = json.dumps({"type": "GetSensorDetails"})
    headers = {
        "Content-Type": "application/json"
    }

    try:
        conn.request("POST", "/", request, headers)
        response = conn.getresponse()
        body = response.read().decode()
        jsonData = json.loads(body)
    except Exception as e:
        log.log("Failed to get sensor details [error: %s]" % (str(e)))
        return network.message(tp, str(e))

    if jsonData.get("type") == "GetSensorDetailsResponse":
        return jsonData
    else:
        return network.message(tp, "SensorDetailsNetworkError")
