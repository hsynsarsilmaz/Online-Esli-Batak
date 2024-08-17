import enum

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
    BIDSKIP = 3
    GAMESTART = 4
    PLAYCARD = 5
    PLAYTURN = 6