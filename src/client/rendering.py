import pygame

from src.client.ui import *
from src.client.gamelogic import *


def renderUiElements(
    elements: list,
    screen: pygame.Surface,
    myTurn: bool = False,
    clickable: bool = False,
    selected=None,
):
    mousePos = pygame.mouse.get_pos()
    for element in elements:
        if myTurn and clickable:
            if element.value == selected or element.rect.collidepoint(mousePos):
                screen.blit(element.highlighted, element.rect)
            else:
                screen.blit(element.normal, element.rect)
        else:
            screen.blit(element.disabled, element.rect)


def renderBidding(screen: pygame.Surface, ui: GameUI, gameState: dict):
    myTurn = gameState["currentPlayer"] == gameState["myId"]
    renderUiElements(ui.biddingNumbers, screen, myTurn, True, gameState["bidRank"])
    renderUiElements(ui.biddingSuits, screen, myTurn, True, gameState["bidSuit"])

    if myTurn:
        renderUiElements([ui.passBidding], screen, myTurn, True)
        renderUiElements([ui.makeBidding], screen, myTurn, True)


def renderCards(decks: dict, screen: pygame.Surface, playingStage: bool):
    selectedCard = None
    if playingStage:
        for card in reversed(decks["my"].cards):
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                selectedCard = card
                break

    for deck in decks.values():
        for card in deck.cards:
            if card.visible:
                if not playingStage:
                    screen.blit(card.image, card.rect)
                elif card.playable:
                    if selectedCard and card == selectedCard:
                        screen.blit(card.image, card.rect.move(0, -20))
                    else:
                        screen.blit(card.image, card.rect)
                else:
                    screen.blit(card.grayImage, card.rect)

            else:
                screen.blit(card.reverse, card.rect)


def renderCardPlayAnimations(
    playAnimations: list,
    destroyAnimations: list,
    screen: pygame.Surface,
    gameState: dict,
):
    for animation in playAnimations:
        if animation.frame < 60:
            animation.rect.x += animation.xVel
            animation.rect.y += animation.yVel
            animation.frame += 1
        elif animation.frame == 60:
            animation.rect.center = (WIDTH // 2, HEIGHT // 2)
            animation.frame += 1

        screen.blit(animation.image, animation.rect)

    if len(playAnimations) >= 4 and playAnimations[3].frame == 61:
        for i in range(4):
            playAnimations[0].calculateWinnerVelocities(
                gameState["myId"], gameState["winner"]
            )
            playAnimations[0].frame = -15 * i
            destroyAnimations.append(playAnimations[0])
            playAnimations.pop(0)


def renderCardDestroyAnimations(
    destroyAnimations: list, screen: pygame.Surface, gameState: dict
):

    for animation in destroyAnimations:
        if animation.frame < 0:
            animation.frame += 1
        elif animation.frame < 60:
            animation.rect.x += animation.xVel
            animation.rect.y += animation.yVel
            animation.frame += 1
        elif animation.frame == 60:
            animation.frame += 1
            if gameState["champion"] != UNDEFINED and len(destroyAnimations) == 0:
                gameState["stage"] = GameStage.END.value

        screen.blit(animation.image, animation.rect)

    if len(destroyAnimations) == 4 and destroyAnimations[3].frame == 61:
        destroyAnimations.clear()
