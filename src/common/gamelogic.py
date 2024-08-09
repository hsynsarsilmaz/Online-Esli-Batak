import enum
class GameState(enum.Enum):
    WAITING = 0
    BIDDING = 1

# Constants
WIDTH, HEIGHT = 1600, 900
FPS = 60
BGCOLOR = (2, 100, 42)
gameState = GameState.WAITING.value
myId = -1
turn = 1

