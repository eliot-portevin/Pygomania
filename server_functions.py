import pickle
HEADER = 16
FORMAT = "utf-8"

class ServerClass:
    def __init__(self):
        self.adress = {}
        self.games = []

    def send(self,msg,client):
        print(f"The message you are trying to send is {msg}.")
        message = pickle.dumps(msg)
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (16 - len(send_length))
        print(f"The encrypted message is {message}")
        print(f"His length is {send_length}")
        client.send(send_length)
        # print(f'The length is {send_length}')
        client.send(message)

    def receive(self,client):
        msg_length = client.recv(16).decode('utf-8')
        if msg_length:
            msg_length = int(msg_length)
            print(f"The message received is {msg_length} characters long.")
            message = client.recv(msg_length)
            print(f"ENCRYPTED MESSAGE RECEIVED : {message}")
            message = pickle.loads(message)
            print(f"DECRYPTED MESSAGE RECEIVED : {message}")
            return message
