import network
import log

import dbest as db


def login(jsonData: dict):
    tp = "LoginResponse"

    id = jsonData.get("id")
    password = jsonData.get("password")

    log.log("Try to login [id: %s]." % (id))

    try:
        db.Database().LoginUser(id, password)
    except Exception as e:
        log.log("Failed to login [id: %s]." % (id))
        return network.message(tp, str(e))

    return network.message(tp, "LoginSucceed")


def register(jsonData: dict):
    tp = "RegisterResponse"

    id = jsonData.get("id")
    password = jsonData.get("password")
    email = jsonData.get("email")
    phoneNumber = jsonData.get("phoneNumber")
    birthday = jsonData.get("birthday")

    log.log("Try to register [id: %s]." % (id))

    try:
        db.Database().AddUser(id, password, birthday, email, phoneNumber)
    except Exception as e:
        log.log("Failed to register [error: %s]." % (str(e)))
        return network.message(tp, str(e))

    return network.message(tp, "RegisterSucceed")


def changeUserInfo(jsonData: dict):
    tp = "ChangeUserInfoResponse"

    id = jsonData.get("id")
    email = jsonData.get("email")
    phoneNumber = jsonData.get("phoneNumber")
    birthday = jsonData.get("birthday")

    log.log("Try to change user info [id: %s]" % (id))

    try:
        db.Database().UpdateUserInfo(id, birthday, phoneNumber, email)
    except Exception as e:
        log.log("Failed to change user info [error: %s]" % (str(e)))
        return network.message(tp, str(e))

    return network.message(tp, "ChangeUserInfoSucceed")
    
def getUserInfo(jsonData: dict):
    tp = "GetUserInfoResponse"
    
    id=jsonData.get("id")
    
    log.log("Try to get user info [id: %s]" % (id))

    try:
        birthday, phoneNumber, email, user_type = db.Database().GetUserInfo(id)
    except Exception as e:
        log.log("Failed to get user info [error: %s]" % (str(e)))
        return network.message(tp, str(e))

    return {
        "birthday": str(birthday),
        "phoneNumber": phoneNumber,
        "email": email
    }
        
