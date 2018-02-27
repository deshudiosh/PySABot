import os
import shutil
from collections import namedtuple

from pathlib import Path

Proxy = namedtuple('Proxy', ["server", "port"])

def getNext():
    fresh = Path("./proxies/fresh/")
    used = Path("./proxies/used/")

    proxy_file = list(fresh.iterdir())[0]

    shutil.move(str(proxy_file), str(Path(used, proxy_file.name)))

    name_split = proxy_file.name.split("-")

    proxy_to_return = Proxy(name_split[0], int(name_split[1]))

    print("Next proxy file taken:", proxy_file.name)

    return proxy_to_return
