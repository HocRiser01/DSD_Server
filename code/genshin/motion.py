import numpy as np

def parseSensor(jsonData: dict):
    data = np.arange(9)
    data[0] = jsonData.get("X")
    data[1] = jsonData.get("Y")
    data[2] = jsonData.get("Z")
    data[3] = jsonData.get("accX")
    data[4] = jsonData.get("accY")
    data[5] = jsonData.get("accZ")
    data[6] = jsonData.get("asX")
    data[7] = jsonData.get("asY")
    data[8] = jsonData.get("asZ")

    return data


def parseMotion(jsonData: dict):
    data = np.arange(55)
    data[ 0: 9] = parseSensor(jsonData.get("L1"))
    data[ 9:18] = parseSensor(jsonData.get("L2"))
    data[18:27] = parseSensor(jsonData.get("L3"))
    data[27:36] = parseSensor(jsonData.get("R1"))
    data[36:45] = parseSensor(jsonData.get("R2"))
    data[45:54] = parseSensor(jsonData.get("R3"))
    data[54] = jsonData.get("timestamp")

    return data

label = ["down", "left", "right", "sit", "stand", "up", "walk"]