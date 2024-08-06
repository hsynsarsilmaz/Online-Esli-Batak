import enum

IP = "localhost"
PORT = 8765
URI = f"ws://{IP}:{PORT}"

#create an enum  for request types
class ReqType(enum.Enum):
    CONNECT = 0
    DISCONNECT = 1