import pygame

from src.client.text import *
from src.client.gamelogic import *


def renderText(items: list, screen: pygame.Surface):
    for text, highligtedText, rect in items:
        if rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(highligtedText, rect)
        else:
            screen.blit(text, rect)


def renderBidding(screen: pygame.Surface, texts: GameText, gameState: dict):
    renderText(texts.biddingNumbers, screen)
    renderText(texts.biddingSuites, screen)

    # Temporary
    if gameState["currentPlayer"] == gameState["myId"]:
        renderText([texts.skipBidding], screen)


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


def renderAnimations(animations: list, screen: pygame.Surface, gameState: dict):
    if gameState["winner"] != UNDEFINED:
        if len(animations) == 4 and animations[3].frame == 61:
            for i, animation in enumerate(animations):
                animation.calculateWinnerVelocities(
                    gameState["myId"], gameState["winner"]
                )
                animation.frame = -15 * i
                animation.destroy = True

    for animation in animations:
        if animation.frame < 0:
            animation.frame += 1
        elif animation.frame < 60:
            animation.rect.x += animation.xVel
            animation.rect.y += animation.yVel
            animation.frame += 1
        elif animation.frame == 60:
            if animation.destroy:
                animations.remove(animation)
                if gameState["champion"] != UNDEFINED and len(animations) == 0:
                    gameState["stage"] = GameStage.END.value
            else:
                animation.xVel = 0
                animation.yVel = 0
                animation.rect.center = (WIDTH // 2, HEIGHT // 2)
                animation.frame += 1

        screen.blit(animation.image, animation.rect)
