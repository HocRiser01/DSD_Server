from . import motion
from . import network

import sys
sys.path.append("..")
import dbest as db


def connectEquipment(jsonData: dict):
    tp = "ConnectEquipmentResponse"

    id = jsonData.get("id")
    ip = jsonData.get("ip")
    equipType = jsonData.get("type")
    port = jsonData.get("port")

    try:
        db.BindDevice(id, ip, port)
    except Exception as e:
        return network.message(tp, str(e))

    return network.message(tp, "ConnectEquipmentSucceed")


def disconnectEquipment(jsonData: dict):
    tp = "DisconnectEquipmentResponse"

    id = jsonData.get("id")

    try:
        db.UnbindDevice(id)
    except Exception as e:
        return network.message(tp, str(e))

    return network.message(tp, "DisconnectEquipmentResponse")
