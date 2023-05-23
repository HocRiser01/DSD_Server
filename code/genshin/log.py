import time
import threading

logLock=threading.Lock()

def log(message: str):
    logLock.acquire()

    with open("log.txt","a") as log:
        currTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        log.write("[%s] %s\n" % (currTime, message))
    log.close()

    logLock.release()
