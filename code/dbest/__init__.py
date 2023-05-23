import numpy as np

def AddUser(user_id: str, password: str, birthday: str, email: str, phone_number: str):
    return

def LoginUser(user_id: str,password: str):
    return

def DeleteUser(user_id: str):
    return

def UpdateUserInfo(user_id: str, birthday: str, phone_number: str, email: str):
    return

def GetUserInfo(user_id: str):
    return "2002.01.01", "mihoyo", "mihoyo@qq.com" # Birthday & Id & Email

def GetMotionData(user_id: str):
    return np.array((1,5,56))

def CleanseData(data):
    return np.array((5,55))

def DeleteMotionRecord(user_id: str, create_time: str):
    return

def SaveMotionData(user_id: str,create_time: str,label: int, data):
    return

def GetDeviceInfo(user_id: str):
    return str, int # IP & Port

def BindDevice(user_id: str,IP: str,Port: str):
    return

def UnbindDevice(user_id: str):
    return

def GetMotionRecord(user_id: str):
    return [1,2], ['a','b'] ,['a','b'] # Label & Creation time & Last time

def ModifyMotionRecord(user_id: str,create_time: str,label:int):
    return

