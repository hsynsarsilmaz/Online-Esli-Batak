import random

from src.common.common import *
from src.server.networking import *
from src.server.game import Game

TBD = ""

def dealCards(cards: list):
    cards.clear()
    suits = ["H", "S", "D", "C"]
    ranks = [int(n) for n in range(2, 15)]
    for suit in suits:
        for rank in ranks:
            cards.append((suit, rank))
    random.shuffle(cards)


async def processBid(myId: int, game: Game, data: dict):
    if data["Data"]["bid"] == UNDEFINED:
        game.bidding.passBid(myId)
    else:
        game.bidding.makeBid(data["Data"]["bid"], data["Data"]["trump"], myId)

    if game.bidding.isBiddingEnded():
        game.turn.trump = game.bidding.trump
        request = ReqType.GAMESTART.value
    else:
        request = ReqType.BIDDING.value

    await broadcast(
        {
            "Type": request,
            "Data": {
                "bid": game.bidding.bid,
                "trump": game.bidding.trump,
                "bidder": game.bidding.bidder,
                "currentPlayer": (
                    game.bidding.currentPlayer
                    if request == ReqType.BIDDING.value
                    else game.bidding.bidder
                ),
            },
        },
        game.connectedClients,
    )


async def playTurn(myId: int, game: Game, data: dict):
    winner = UNDEFINED
    champion = UNDEFINED
    game.turn.play(data["Data"]["suit"], data["Data"]["rank"], myId)
    if game.turn.playedCount == 4:
        winner = game.turn.winner
        if winner == 0 or winner == 2:
            game.points[0] += 1
        else:
            game.points[1] += 1
        game.turn.endTurn()
        if game.turn.number == 13:
            if game.bidding.bidder == 0 or game.bidding.bidder == 2:
                if game.points[0] < game.bidding.bid:
                    game.points[0] = -game.bidding.bid
                if game.points[1] < 2:
                    game.points[1] = -game.bidding.bid
            else:
                if game.points[0] < 2:
                    game.points[0] = -game.bidding.bid
                if game.points[1] < game.bidding.bid:
                    game.points[1] = -game.bidding.bid

            starter = game.bidding.starter + 1 % 4
            game.bidding.reset(starter)
            dealCards(game.cards)

            await broadcast(
                {
                    "Type": ReqType.ENDROUND.value,
                    "Data": {
                        "suit": game.turn.turnSuit,
                        "rank": game.turn.lastRank,
                        "biggestRank": game.turn.biggestRank,
                        "originalSuit": game.turn.originalSuit,
                        "isTrumpPlayed": game.turn.isTrumpPlayed,
                        "currentPlayer": game.turn.currentPlayer,
                        "winner": winner,
                        "champion": champion,
                        "isFirstTurn": game.turn.playedCount == 0,
                        "points": game.points,
                        "cards": game.cards,
                        "starterId": game.bidding.starter,
                    },
                },
                game.connectedClients,
            )

            game.turn.reset()

            return

    await broadcast(
        {
            "Type": ReqType.PLAYTURN.value,
            "Data": {
                "suit": game.turn.turnSuit,
                "rank": game.turn.lastRank,
                "biggestRank": game.turn.biggestRank,
                "originalSuit": game.turn.originalSuit,
                "isTrumpPlayed": game.turn.isTrumpPlayed,
                "currentPlayer": game.turn.currentPlayer,
                "winner": winner,
                "champion": champion,
                "isFirstTurn": game.turn.playedCount == 0,
            },
        },
        game.connectedClients,
    )
