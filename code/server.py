import sys
sys.path.append(".")
sys.path.append("./AI")
sys.path.append("./dbest")
sys.path.append("./genshin")

import traceback
import importlib
import json
import threading
import socket
import genshin

HOST = "0.0.0.0"
PORT = 11451
MBUF = 1048576 * 10  # Max buffer size 10MB

def parse(jsonData: dict):
    if type(jsonData) is not dict:
        return {
            "type": "Error",
            "network.message": "RequestObjectIsNotJson"
        }

    if type(jsonData.get("type")) == str:
        jsonType = jsonData.get("type")

        if jsonType == "Login":
            return genshin.login(jsonData)
        elif jsonType == "Register":
            return genshin.register(jsonData)
        elif jsonType == "ChangeUserInfo":
            return genshin.changeUserInfo(jsonData)
        elif jsonType == "ConnectEquipment":
            return genshin.connectEquipment(jsonData)
        elif jsonType == "DisconnectEquipment":
            return genshin.disconnectEquipment(jsonData)
        elif jsonType == "GetData":
            return genshin.getData(jsonData)
        elif jsonType == "DiscardData":
            return genshin.discardData(jsonData)
        elif jsonType == "ChangeLabel":
            return genshin.changeLabel(jsonData)
        elif jsonType == "CollectData":
            return genshin.collectData(jsonData)
        elif jsonType == "CollectDataStop":
            return genshin.collectDataStop(jsonData)
        elif jsonType == "GetPrediction":
            return genshin.getPrediction(jsonData)
        elif jsonType == "GetSensorDetails":
            return genshin.getSensorDetails(jsonData)
        elif jsonType == "GetSensorStatus":
            return genshin.getSensorStatus(jsonData)
        else:
            return {
                "type": "Error",
                "network.message": "RequestTypeUnknown",
                "details": str(jsonType)
            }
    else:
        return {
            "type": "Error",
            "network.message": "JsonDataHasNoAttributeType"
        }


def solve(bodydata: str):
    try:
        jsonData = json.loads(bodydata)
    except:
        jsonData = None

    if jsonData is None:
        return {
            "type": "Error",
            "network.message": "PostDataIsNotJson"
        }

    if type(jsonData) == dict and jsonData.get("type") == "Reload":
        try:
            importlib.reload(genshin)
            ans = {
                "type": "ReloadResponse",
                "network.message": "ReloadSucceed"
            }
        except:
            ans = None
            errorDetail = str(traceback.format_exc())
    else:
        try:
            ans = parse(jsonData)
            errorDetail = "ServerProcessFuctionForgetToReturn"
        except:
            ans = None
            errorDetail = str(traceback.format_exc())

    if ans is not None:
        return ans
    else:
        return {
            "type": "Error",
            "network.message": "ServerInnerError",
            "details": errorDetail
        }


def work(conn, addr):
    data = conn.recv(MBUF).decode()

    try:
        bodydata = data.split("\r\n\r\n", 1)[1]
    except:
        bodydata = None

    if bodydata is not None:
        ans = solve(bodydata)
    else:
        ans = {
            "type": "Error",
            "network.message": "NoPostData"
        }

    dataToSend = json.dumps(ans).encode()
    httpHeader = "HTTP/1.1 200 OK\r\n"
    httpHeader += "Content-Type: application/json\r\n"
    httpHeader += "Content-Length: " + str(len(dataToSend))
    mergedData = (httpHeader + "\r\n\r\n").encode() + dataToSend
    conn.sendall(mergedData)
    conn.close()
    genshin.log(f"Closing {addr}.")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    genshin.log(f"Listening {HOST}:{PORT}.")
    while True:
        conn, addr = sock.accept()
        genshin.log(f"Connected by {addr}.")
        t = threading.Thread(target=work, args=(conn, addr))
        t.start()
