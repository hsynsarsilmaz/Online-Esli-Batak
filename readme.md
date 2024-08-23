# Eşli Batak

**Eşli Batak** is a variation of the popular Turkish card game Batak. The game is played with 2 teams, each consisting of 2 players. The objective is to score the most points by winning tricks while avoiding falling short of your team's bid, which results in penalty points.

## Complete Ruleset of Game
[Ruleset](https://github.com/hsynsarsilmaz/Online-Esli-Batak/blob/main/doc/Ruleset.pdf)

## How to Run the Game

The game operates on a LAN, and 4 players are needed to start.

1. **Start the server:**
   - [Link to server executable will be added]

2. **Run the game executable and connect to the server using its IP address:**
   - [Link to client executable will be added]

## How to Find the Server IP

- **On Windows:** Use the `ipconfig` command.
- **On Linux:** Use the `ifconfig` command.

## Running the Game with Python

To run the game directly with Python, ensure you have the `websockets` and `pygame` modules installed:

```bash
pip install pygame websockets
python -m src.server.main
python -m src.client.main 
```

![Screenshot 1](https://raw.githubusercontent.com/hsynsarsilmaz/Online-Esli-Batak/main/res/img/misc/ss1.png)
![Screenshot 2](https://raw.githubusercontent.com/hsynsarsilmaz/Online-Esli-Batak/main/res/img/misc/ss2.png)