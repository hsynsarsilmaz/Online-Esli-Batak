import websockets
import json

from src.client.ui import *
from .round import *


async def handleServerConnection(
    websocket: websockets.WebSocketClientProtocol,
    round: Round,
    ui: GameUI,
    cardPlayAnimations: list,
):
    async for message in websocket:
        data = json.loads(message)

        if data["Type"] == ReqType.CONNECT.value:
            round.assignMyId(data["Data"])

        elif data["Type"] == ReqType.START.value:
            round.startNewRound(data)

        elif data["Type"] == ReqType.BIDDING.value:
            round.startBiddingStage(data)

        elif data["Type"] == ReqType.GAMESTART.value:
            round.startPlayingStage(data)

        elif data["Type"] == ReqType.PLAYTURN.value:
            round.playTurn(data, ui, cardPlayAnimations)

        elif data["Type"] == ReqType.ENDROUND.value:
            round.playTurn(data, ui, cardPlayAnimations)
            round.endRound(data)
