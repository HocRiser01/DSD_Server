# This is a demo for CentralServer

import genshin
import socket
import threading
import json
import importlib
import traceback

HOST = 'localhost'
PORT = 12345
MBUF = 1048576 * 10  # Max buffer size 10MB

def parse(jsonData: dict):
    # check type == dict
    if type(jsonData) is not dict:
        return {
            "type": "Error",
            "network.message": "RequestObjectIsNotJson"
        }
    # calculate and get the response value
    if type(jsonData.get("type")) == str:
        if jsonData.get("type") == "Login":
            return genshin.login(jsonData)
        elif jsonData.get("type") == "Register":
            return genshin.register(jsonData)
        elif jsonData.get("type") == "ChangeUserInfo":
            return genshin.changeUserInfo(jsonData)
        elif jsonData.get("Type") == "ConnectEquipment":
            return genshin.connectEquipment(jsonData)
        elif jsonData.get("Type") == "DisconnectEquipment":
            return genshin.disconnectEquipment(jsonData)
        elif jsonData.get("type") == "GetData":
            return genshin.genshin.getData(jsonData)
        elif jsonData.get("type") == "DiscardData":
            return genshin.discardData(jsonData)
        elif jsonData.get("type") == "ChangeLabel":
            return genshin.changeLabel(jsonData)
        elif jsonData.get("Type") == "CollectData":
            return genshin.collectData(jsonData)
        elif jsonData.get("Type") == "CollectDataStop":
            return genshin.collectDataStop(jsonData)
        elif jsonData.get("Type") == "GetPrediction":
            return genshin.getPrediction(jsonData)
        else:
            return {
                "type": "Error",
                "network.message": "RequestTypeUnknown",
                "details": str(jsonData.get("type"))
            }
    else:
        return {
            "type": "Error",
            "network.message": "JsonDataHasNoAttributeType"
        }



def solve(bodydata: str):
    # try to get json data
    try:
        jsonData = json.loads(bodydata)
    except:
        jsonData = None
    # if can not get json data
    if jsonData is None:
        return {
            "type": "Error",
            "network.message": "PostDataIsNotJson"
        }
    # form ans
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
    # return ans to the client
    if ans is not None:
        return ans
    else:
        return {
            "type": "Error",
            "network.message": "ServerInnerError",
            "details": errorDetail
        }


# calculate the return value
def work(conn, addr):
    data = conn.recv(MBUF).decode()
    # print(f"[.] debug get data = {data}")
    # get body data
    try:
        bodydata = data.split("\r\n\r\n", 1)[1]
    except:
        bodydata = None
    print(f"[.] debug get addr = {addr} data = {bodydata}")
    # get response for the request
    if bodydata is not None:
        ans = solve(bodydata)
    else:
        ans = {
            "type": "Error",
            "network.message": "NoPostData"
        }
    # parse data
    dataToSend = json.dumps(ans).encode()
    httpHeader = "HTTP/1.1 200 OK\r\n"
    httpHeader += "Content-Type: application/json\r\n"
    httpHeader += "Content-Length: " + str(len(dataToSend))
    mergedData = (httpHeader + "\r\n\r\n").encode() + dataToSend
    conn.sendall(mergedData)
    conn.close()
    print(f"[-] closing {addr}")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f"[.] listening {HOST}:{PORT}")
    while True:
        conn, addr = sock.accept()
        print(f"[+] connected by {addr}")
        t = threading.Thread(target=work, args=(conn, addr))
        t.start()