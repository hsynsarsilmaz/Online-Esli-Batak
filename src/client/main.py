import pygame
import asyncio
import websockets
import json


from ..common.networking import * 

WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
color = WHITE

async def handleIncomingMessages(websocket : websockets.WebSocketClientProtocol):
    global color
    async for message in websocket:
        data = json.loads(message)
        if(data["Test"] == "Hello, client!"):
            print(f"Received from server: {data}")
            message = json.dumps({"Test": "Hello, server!"})
            await asyncio.sleep(5)
            await websocket.send(message)
            print(f"Sent message to server: {message}")
            color = BLACK

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")
clock = pygame.time.Clock()

async def main():
    async with websockets.connect(URI) as websocket:

        message_handler = asyncio.create_task(handleIncomingMessages(websocket))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            screen.fill(color)
            pygame.display.flip()
            clock.tick(FPS)

            await asyncio.sleep(0)

        await websocket.close()

if __name__ == "__main__":
    asyncio.run(main())