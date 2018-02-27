import datetime
import os

from proxy_servers import Proxy


def make_proxy_log(success, reason:str, proxy: Proxy, start:datetime):

    directory = "./proxy_logs"
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.datetime.now()

    duration = now - start

    now = now.strftime("%Y-%m-%d %H-%M-%S")

    p = "./proxy_logs/{} {} {} {} {}".format(
        now,
        "SUCCESS" if success else "FAIL",
        reason,
        "{}-{}".format(proxy.server, proxy.port),
        "{}sec".format(duration.seconds)
    )

    with open(p, "w+") as f:
        print(p)

