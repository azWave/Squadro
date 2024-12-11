import argparse
import socket
import random
from string import ascii_uppercase , digits

Name = "".join(random.choices(ascii_uppercase + digits, k=6))
parser = argparse.ArgumentParser(
                prog='Squadro Game Socket Server',
                description='Simple prompt Squadro game')
parser.add_argument("-N", "--name", type=str, default=Name)

args = parser.parse_args()


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 12345))
print(clientsocket.recv(1024).decode("utf-8"))
print(args.name)

clientsocket.send(args.name.encode("utf-8"))
print(clientsocket.recv(1024).decode("utf-8"))
while True:
    try:
        print(clientsocket.recv(1024).decode("utf-8"))
        output = input("Enter a message: ")
        clientsocket.send(output.encode("utf-8"))
    except KeyboardInterrupt:
        clientsocket.close()
        print("Connection closed.")
        break

    