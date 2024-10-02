
# 🎴 Eşli Batak

**Eşli Batak** is an exciting variation of the popular Turkish card game **Batak**. Played with two teams of two players each, the goal is to score the most points by winning tricks while avoiding falling short of your team's bid, which can lead to penalty points.

## 📝 Complete Ruleset
For a detailed overview of the game's rules, check out the [Complete Ruleset](https://github.com/hsynsarsilmaz/Online-Esli-Batak/blob/main/doc/Ruleset.pdf).

## 🚀 How to Run the Game

The game operates on a Local Area Network (LAN) and requires **4 players** to start. Follow these steps to get started:

1. **Start the Server**: The server will run on port **7777** on localhost.
2. **Start the Clients**: Once the server is running, you can start the clients. The clients will automatically connect to the server and wait for other players. The game begins when **4 clients** are connected.

### 🔗 Download Link
- [Latest Release](https://github.com/hsynsarsilmaz/Online-Esli-Batak/releases/tag/v1.0)

## 🐍 Running the Game with Python

To run the game directly using Python, make sure you have the `websockets` and `pygame` modules installed. You can do this by running:

```bash
pip install pygame websockets
```

Then, you can start the server and clients with the following commands:

```bash
python -m src.server.main
python -m src.client.main 
```

## 📸 Screenshots
![Screenshot 1](https://raw.githubusercontent.com/hsynsarsilmaz/Online-Esli-Batak/main/res/img/misc/ss1.png)
![Screenshot 2](https://raw.githubusercontent.com/hsynsarsilmaz/Online-Esli-Batak/main/res/img/misc/ss2.png)
