import socket
import threading
import pickle

HEADER = 16
PORT = 10632
SERVER = '0.0.0.0'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

DISCONNECT_MSG = '!DISCONNECT'


class ServerClass:
    def __init__(self):
        self.adress = {}
        self.games = {}

    def send(self,msg,client):
        print(f"The message you are trying to send is {msg}.")
        message = pickle.dumps(msg)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        print(f"The encrypted message is {message}")
        print(f"His length is {send_length}")
        client.send(send_length)
        # print(f'The length is {send_length}')
        client.send(message)

    def receive(self,msg,client):
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            print(f"The message received is {msg_length} characters long.")
            message = client.recv(msg_length)
            print(f"ENCRYPTED MESSAGE RECEIVED : {message}")
            message = pickle.loads(message)
            print(f"DECRYPTED MESSAGE RECEIVED : {message}")
            return message
