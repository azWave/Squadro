from classes.server import SquadroGameServer
from classes.game import SquadroGame
import argparse


parser = argparse.ArgumentParser(
                prog='Squadro Game Socket Server',
                description='Simple prompt Squadro game')
parser.add_argument("-ip", "--ip", type=str, default="localhost")
parser.add_argument("-p", "--port", type=int, default=12345)
parser.add_argument('-s', '--server',action='store_true')
parser.add_argument('-t', '--tutorial',action='store_true')

args = parser.parse_args()

if args.server:
    server = SquadroGameServer(args)
    server.run()
else :
    game = SquadroGame(args)
    game.run()
