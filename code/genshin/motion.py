def parseSensor(jsonData: dict):
    data = np.full((9), 0)
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
    data = np.full((55))
    data[9*0:9*1-1] = parseSensor(jsonData.get("L1"))
    data[9*1:9*2-1] = parseSensor(jsonData.get("L2"))
    data[9*2:9*3-1] = parseSensor(jsonData.get("L3"))
    data[9*3:9*4-1] = parseSensor(jsonData.get("R1"))
    data[9*4:9*5-1] = parseSensor(jsonData.get("R2"))
    data[9*5:9*6-1] = parseSensor(jsonData.get("R3"))
    data[54] = jsonData.get("timestamp")

    return data

label = ["down", "left", "right", "sit", "stand", "up", "walk"]