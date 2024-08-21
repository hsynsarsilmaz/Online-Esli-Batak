import enum
import sys
import os

# Constants
WIDTH, HEIGHT = 1600, 900
FPS = 60
BGCOLOR = (2, 100, 42)
UNDEFINED = -1

IP = "localhost"
PORT = 7777
URI = f"ws://{IP}:{PORT}"
BUILD = False

class ReqType(enum.Enum):
    CONNECT = 0
    DISCONNECT = 1
    START = 2
    MAKEBID = 3
    BIDDING = 4
    GAMESTART = 5
    PLAYCARD = 6
    PLAYTURN = 7


def resourcePath(relativePath):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relativePath)
