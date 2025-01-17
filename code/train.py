import sys
sys.path.append(".")
sys.path.append("./AI")
sys.path.append("./dbest")
sys.path.append("./genshin")

import threading
import dbest as db
import AI as ai
import genshin

def train(id: str):
    data = db.Database().GetMotionData(id)
    
    try: 
        if data.shape[0] == 0:
            genshin.log("No data collected for %s. Skip." % id)
            return
    except:
        genshin.log("No data collected for %s. Skip." % id)
        return

    train_time = ai.get_train_time(data)
    genshin.log(
        "Start to train model of %s [expected training time: %d sec]." % (id, train_time))
    try:
        acc, logPath = ai.get_train(id, data)
    except Exception as e:
        genshin.log("Failed to train model [error: %s]." % (str(e)))
        return
    
    genshin.log("Training finished [id: %s, accuarcy: %f, log path: %s]." % (id, acc, logPath))


if __name__ == "__main__":
    users = db.Database().GetallUser()
    
    for user in users:
        train_thread = threading.Thread(target=train, args=(user))
        train_thread.start()
