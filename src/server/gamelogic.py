import pygame
import asyncio
import websockets
import random

from ..common.networking import *
from ..common.card import *
from ..common.gamelogic import *
from ..common.text import *

from .networking import *


def dealCards(cards: list):
    suits = ["H", "S", "D", "C"]
    ranks = [int(n) for n in range(2, 15)]
    for suit in suits:
        for rank in ranks:
            cards.append((suit, rank))
    random.shuffle(cards)


async def skipBid(myId: int, connectedClients: list, turn: Turn, data: dict):
    print(f"Player {myId + 1} skipped bidding")
    turn.trump = data["Data"]["trump"]
    await broadcast(
        {
            "Type": ReqType.GAMESTART.value,
            "Data": {
                "bid": data["Data"]["bid"],
                "trump": data["Data"]["trump"],
                "bidder": myId,
            },
        },
        connectedClients,
    )


async def playTurn(
    myId: int, connectedClients: list, turn: Turn, data: dict, points: list
):
    winner = UNDEFINED
    champion = UNDEFINED
    turn.play(data["Data"]["suit"], data["Data"]["rank"], myId)
    if turn.playedCount == 4:
        winner = turn.winner
        if winner == 0 or winner == 2:
            points[0] += 1
        else:
            points[1] += 1
        turn.endTurn()
        if turn.number == 13:
            if points[0] > points[1]:
                champion = 0
            else:
                champion = 1

    await broadcast(
        {
            "Type": ReqType.PLAYTURN.value,
            "Data": {
                "suit": turn.lastSuit,
                "rank": turn.lastRank,
                "currentPlayer": turn.currentPlayer,
                "winner": winner,
                "champion": champion,
                "isFirstTurn": turn.playedCount == 0,
            },
        },
        connectedClients,
    )
