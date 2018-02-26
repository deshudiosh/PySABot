import datetime
import os


def make_log_file(success):
    directory = "./logs"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    p = "./logs/{} {}".format(now, "success" if success else "fail")

    with open(p, "w+") as f:
        print(p)

