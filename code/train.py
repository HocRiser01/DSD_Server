import threading
import dbest as db
import AI as ai
import genshin
import sys
sys.path.append(".")
sys.path.append("./AI")
sys.path.append("./dbest")
sys.path.append("./genshin")


def train(id: str):
    data = db.Database().GetMotionData(id)
    train_time = ai.get_train_time(data)
    genshin.log.log(
        "Start to train model of %s [expected training time: %d sec]." % (id, train_time))
    try:
        acc, logPath = ai.get_train(id, data)
    except Exception as e:
        genshin.log.log("Failed to train model [error: %s]." % (str(e)))
    genshin.log.log("Training finished [id: %s]." % (id))
    return


if __name__ == "__main__":
    users = db.Database().GetAllUser()

    for user in users:
        train_thread = threading.Thread(target=train, args=(user))
        train_thread.start()
