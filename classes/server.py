import argparse
import socket
import threading
import logging
from classes.game import SquadroGame

class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


class SquadroGameServer:
    def __init__(self, args,nbrSynClients = 2):
        self.args = args
        self.host = args.ip
        self.port = args.port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(nbrSynClients)
        self.clients = []
        self.initLogger()
        
    def initLogger(self):
        self.logger = logging.getLogger("SquadroServer")
        self.logger.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(LoggingFormatter())
        # File handler
        file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
        file_handler_formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
        )
        file_handler.setFormatter(file_handler_formatter)

        # Add the handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def registerClient(self,client):
        client.send(b"Welcome to Squadro!\n\r What is your name ?")
        name = client.recv(1024).decode("utf-8")
        self.logger.info(f"Player {name} connected.")
        self.clients.append({"name":name,"conn":client})

    def run(self):
        self.logger.info(f"Listening on {self.host}:{self.port}...")
        self.clients = []
        while True:
            client, addr = self.server_socket.accept()
            self.logger.info(f"Accepted connection from {addr[0]}:{addr[1]}")
            self.registerClient(client)
            if len(self.clients) >= 2:
                self.logger.info("Starting game...")
                self.logger.info(f"Players: {self.clients[:2]}")
                clients_handler = threading.Thread(target=self.match, args=(self.clients[:2],))
                clients_handler.start()
                del self.clients[:2]

    def match(self,players):
        try:
            game = SquadroGame(self.args)
            playersName  = ",".join([p["name"] for p in players])
            self.logger.info(f"Game started!\n\r players: {playersName}")
            for p in players:
                message = f"{p['name']} you are player {players.index(p) + 1}.\n\r Game starting!"
                p["conn"].send(bytes(message, "utf-8"))
            while True:
                for currentPlayer in players:
                    currentPlayer["conn"].send(bytes(str(game.board), "utf-8"))
                    data = currentPlayer["conn"].recv(1024).decode("utf-8")
                    self.logger.info(f"From {currentPlayer['name']},Received: {data}")
                    game.play_turn(data)
                    game.change_turn()
                if game.board.is_win:
                    self.logger.info(f"Game over!\r\n Winner: {currentPlayer['name']}")
                    currentPlayer["conn"].send(b"You win!")
                    currentPlayerIndex = players.index(currentPlayer)
                    players[currentPlayerIndex + 1 % 2]["conn"].send(b"You lose!")
                    break


        except Exception as e:
            self.logger.error(f"Error handling client: {e}")

        finally:
            for p in players:
                p.close()
