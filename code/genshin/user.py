from .import network

import sys
sys.path.append("..")
import dbest as db

def login(jsonData: dict):
    tp = "LoginResponse"

    id = jsonData.get("id")
    password = jsonData.get("password")

    try:
        db.LoginUser(id, password)
    except Exception as e:
        return network.message(tp, str(e))

    return network.message(tp, "LoginSucceed")


def register(jsonData: dict):
    tp = "RegisterResponse"

    id = jsonData.get("id")
    password = jsonData.get("password")
    username = jsonData.get("username")
    email = jsonData.get("email")
    phoneNumber = jsonData.get("phoneNumber")
    birthday = jsonData.get("birthday")

    try:
        db.AddUser(userId, password, birthday, email, phoneNumber)
    except Exception as e:
        return network.message(tp, str(e))

    return network.message(tp, "RegisterSucceed")


def changeUserInfo(jsonData: dict):
    tp = "ChangeUserInfoResponse"

    id = jsonData.get("id")
    password = jsonData.get("password")
    username = jsonData.get("username")
    email = jsonData.get("email")
    phoneNumber = jsonData.get("phoneNumber")
    birthday = jsonData.get("birthday")

    try:
        db.UpdateUserInfo(id, password, birthday, email, phoneNumber)
    except Exception as e:
        return network.message(tp, str(e))

    return network.message(tp, "ChangeUserInfoSucceed")