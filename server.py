import socket
import threading
import pickle

HEADER = 16
PORT = 10632
# SERVER = '0.0.0.0'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

DISCONNECT_MSG = '!DISCONNECT'
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


class ServerClass:
    def __init__(self):
        self.adress = {}
        self.ingame = {}
        self.games = {}

    def send(self, msg, client):
        print(f"SENDING : {msg} to {client}.")
        message = pickle.dumps(msg)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        # print(f"The encrypted message is {message}")
        # print(f"His length is {send_length}")
        client.send(send_length)
        # print(f'The length is {send_length}')
        client.send(message)

    def receive(self, client):
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # print(f"The message received is {msg_length} characters long.")
            message = client.recv(msg_length)
            # print(f"ENCRYPTED MESSAGE RECEIVED : {message}")
            message = pickle.loads(message)
            # print(f"DECRYPTED MESSAGE RECEIVED : {message}")
            return message


s = ServerClass()


def handle_clients(conn, addr):
    connected = True
    while connected:
        message = s.receive(conn)
        print(f"RECEIVED : {message} from {addr}")
        if message == DISCONNECT_MSG:
            for i in s.games.values():
                if conn in i:
                    s.send(DISCONNECT_MSG, i[i.index(conn) + 1 % 2])
                    del s.games[message[1]]
            if conn in s.ingame.keys():
                del s.ingame[conn]
            connected = False
        elif message[0] == "Play":
            game = s.games[s.ingame[conn]]
            s.send(message[1], game[(game.index(conn) + 1) % 2])
        elif message == "Games":
            s.send(list(s.games.keys()), conn)
        elif message[0] == "Create":
            s.games[message[1]] = [conn]
            s.ingame[conn] = message[1]
        elif message[0] == "join":
            if message[1] in s.games.keys():
                s.games[message[1]].append(conn)
                s.ingame[conn] = message[1]
                for i in s.games[message[1]]:
                    s.send(True, i)
            else:
                s.send(False, conn)


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        s.adress[conn] = s.receive(conn)
        thread = threading.Thread(target=handle_clients, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] The server is starting...")
start()
