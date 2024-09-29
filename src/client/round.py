from .card import *
from src.common.common import *
from .ui import GameUI
from .deck import *


class Round:
    def __init__(self) -> None:
        self.gameState = self.getDefaultGameState()
        self.decks = {}

    def getDefaultGameState(self) -> dict:
        return {
            "myId": UNDEFINED,
            "currentPlayer": 0,
            "stage": GameStage.WAITING.value,
            "bid": UNDEFINED,
            "trump": TBD,
            "bidder": UNDEFINED,
            "winner": UNDEFINED,
            "champion": UNDEFINED,
            "bidSuit": "",
            "bidRank": UNDEFINED,
            "points": [0, 0],
            "endRound": False,
            "newRound": False,
            "newRoundData": {},
        }

    def clearRoundData(self):
        self.gameState = self.getDefaultGameState()
        self.decks = {}

    def loadNextRound(self, ui: GameUI):
        points = self.gameState["points"]
        myId = self.gameState["myId"]
        starterId = self.gameState["newRoundData"]["starterId"]
        points[0] += self.gameState["newRoundData"]["points"][0]
        points[1] += self.gameState["newRoundData"]["points"][1]
        ui.updatePoints(points)
        cards = self.loadCardImages(self.gameState["newRoundData"]["cards"])
        self.clearRoundData()
        self.dealCards(cards, myId)
        self.gameState["myId"] = myId
        self.gameState["points"] = points
        self.gameState["stage"] = GameStage.BIDDING.value
        self.gameState["bid"] = UNDEFINED
        self.gameState["trump"] = TBD
        self.gameState["bidder"] = UNDEFINED
        self.gameState["currentPlayer"] = starterId

    def rePositionCards(self):
        for key, deck in self.decks.items():
            played = 13 - len(deck.cards)
            if key == "my":
                for i, card in enumerate(deck.cards):
                    card.rect.midleft = (
                        deck.initPos + i * deck.interval + played * deck.factor,
                        deck.fixedPos,
                    )
            elif key == "left":
                for i, card in enumerate(deck.cards):
                    card.rect.midtop = (
                        deck.fixedPos,
                        deck.initPos + i * deck.interval + played * deck.factor,
                    )
            elif key == "mate":
                for i, card in enumerate(deck.cards):
                    card.rect.midleft = (
                        deck.initPos + i * deck.interval + played * deck.factor,
                        deck.fixedPos,
                    )
            elif key == "right":
                for i, card in enumerate(deck.cards):
                    card.rect.midtop = (
                        deck.fixedPos,
                        deck.initPos + i * deck.interval + played * deck.factor,
                    )

    def dealCards(self, cards: list, myId: int):
        cardReverseVertical, cardReverseHorizontal = self.loadCardReverseImages()
        self.decks["my"] = Deck()
        self.decks["left"] = Deck()
        self.decks["mate"] = Deck()
        self.decks["right"] = Deck()

        for i in range(4):
            for j in range(13):
                card = cards[j + i * 13]
                if i == myId:
                    card.reverse = cardReverseVertical
                    card.visible = True
                    self.decks["my"].cards.append(card)
                elif i == (myId + 1) % 4:
                    card.reverse = cardReverseHorizontal
                    self.decks["left"].cards.append(card)
                elif i == (myId + 2) % 4:
                    card.reverse = cardReverseVertical
                    self.decks["mate"].cards.append(card)
                elif i == (myId + 3) % 4:
                    card.reverse = cardReverseHorizontal
                    self.decks["right"].cards.append(card)

        for deck in self.decks.values():
            deck.sortDeck()

        self.decks["my"].initialPositions("my")
        self.decks["left"].initialPositions("left")
        self.decks["mate"].initialPositions("mate")
        self.decks["right"].initialPositions("right")
        self.rePositionCards()

    def assignMyId(self, myId: int):
        self.gameState["myId"] = myId

    def loadCardReverseImages(self):
        relativePath = "res/img/cards/RV.png"
        path = resourcePath(relativePath)

        cardReverse = pygame.image.load(path if BUILD else relativePath).convert_alpha()
        cardReverse = pygame.transform.scale(cardReverse, (CARD_WIDTH, CARD_HEIGHT))

        return cardReverse, pygame.transform.rotate(cardReverse, 90)

    def loadCardImages(self, SuitsAndRanks):
        cards = []
        for suit, rank in SuitsAndRanks:
            relativePath = f"res/img/cards/{rank}{suit}.png"
            path = resourcePath(relativePath)
            image = pygame.image.load(path if BUILD else relativePath).convert_alpha()
            image = pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))
            cards.append(Card(suit, rank, image))

        return cards

    def startNewRound(self, data: dict):
        cards = self.loadCardImages(data["Data"]["cards"])
        self.dealCards(cards, self.gameState["myId"])
        self.gameState["stage"] = GameStage.BIDDING.value
        self.gameState["bid"] = UNDEFINED
        self.gameState["trump"] = TBD
        self.gameState["bidder"] = UNDEFINED
        self.gameState["currentPlayer"] = data["Data"]["starterId"]

    def startBiddingStage(self, data: dict):
        self.gameState["bid"] = data["Data"]["bid"]
        self.gameState["trump"] = data["Data"]["trump"]
        self.gameState["bidder"] = data["Data"]["bidder"]
        self.gameState["bidRank"] = UNDEFINED
        self.gameState["bidSuit"] = TBD
        self.gameState["currentPlayer"] = data["Data"]["currentPlayer"]

    def startPlayingStage(self, data: dict):
        self.gameState["bid"] = data["Data"]["bid"]
        self.gameState["trump"] = data["Data"]["trump"]
        self.gameState["bidder"] = data["Data"]["bidder"]
        self.gameState["stage"] = GameStage.PLAYING.value
        self.gameState["currentPlayer"] = data["Data"]["currentPlayer"]
        if self.gameState["myId"] == self.gameState["currentPlayer"]:
            self.decks["my"].markPlayableCards(
                True, "", 0, self.gameState["trump"], False, ""
            )

    def playTurn(self, data: dict, ui: GameUI, cardPlayAnimations: list):
        self.gameState["currentPlayer"] = data["Data"]["currentPlayer"]
        if self.gameState["currentPlayer"] != self.gameState["myId"]:
            self.decks["my"].unMarkMyCards()
        else:
            self.decks["my"].markPlayableCards(
                data["Data"]["isFirstTurn"],
                data["Data"]["suit"],
                data["Data"]["biggestRank"],
                self.gameState["trump"],
                data["Data"]["isTrumpPlayed"],
                data["Data"]["originalSuit"],
            )
        card = None
        for key, deck in self.decks.items():
            card = deck.findCard(data["Data"]["suit"], data["Data"]["rank"])
            if card:
                deck.cards.remove(card)
                break
        card.xVel = (WIDTH // 2 - card.rect.center[0]) / 60
        card.yVel = (HEIGHT // 2 - card.rect.center[1]) / 60
        card.frame = 0
        card.rect = card.image.get_rect(center=card.rect.center)

        cardPlayAnimations.append(card)

        self.gameState["winner"] = data["Data"]["winner"]
        self.gameState["champion"] = data["Data"]["champion"]

        if self.gameState["champion"] != UNDEFINED:
            self.gameState["champion"] = data["Data"]["champion"]
            ui.createWinner(self.gameState["champion"])

        self.rePositionCards()

    def endRound(self, data: dict, ui: GameUI, cardPlayAnimations: list):
        self.gameState["currentPlayer"] = data["Data"]["currentPlayer"]
        if self.gameState["currentPlayer"] != round.gameState["myId"]:
            self.decks["my"].unMarkMyCards()
        else:
            self.decks["my"].markPlayableCards(
                data["Data"]["isFirstTurn"],
                data["Data"]["suit"],
                data["Data"]["biggestRank"],
                self.gameState["trump"],
                data["Data"]["isTrumpPlayed"],
                data["Data"]["originalSuit"],
            )
        card = None
        for key, deck in self.decks.items():
            card = deck.findCard(data["Data"]["suit"], data["Data"]["rank"])
            if card:
                deck.cards.remove(card)
                break
        card.xVel = (WIDTH // 2 - card.rect.center[0]) / 60
        card.yVel = (HEIGHT // 2 - card.rect.center[1]) / 60
        card.frame = 0
        card.rect = card.image.get_rect(center=card.rect.center)

        cardPlayAnimations.append(card)

        self.gameState["winner"] = data["Data"]["winner"]
        self.gameState["champion"] = data["Data"]["champion"]

        if self.gameState["champion"] != UNDEFINED:
            self.gameState["champion"] = data["Data"]["champion"]
            ui.createWinner(self.gameState["champion"])

        self.rePositionCards()

        self.gameState["endRound"] = True
        self.gameState["newRoundData"] = data["Data"]
