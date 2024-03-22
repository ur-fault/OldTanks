import socket
import pickle
import sys


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = input("Write host's IP: ")
        self.port = 5555
        self.addr = (self.server, self.port)
        self.bytes = 2048
        print("Trying:", self.addr)
        self.order = self.connect()
        print("Recieved All data")
        print(str(self.order))

    def get_data(self):
        return self.data

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected")
            return pickle.loads(self.client.recv(self.bytes))
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            msg = pickle.dumps(data)
            self.client.send(msg)
            # print("Sent:", str(data))
            # return self.recvieve()
        except socket.error as e:
            print(e)

    def recvieve(self):
        try:
            msg = self.client.recv(self.bytes)
            data = pickle.loads(msg)
            # print("Got this list:", data)
            return data
        except socket.error as e:
            print(e)
            sys.exit()
        except pickle.UnpicklingError as e:
            data = msg.decode("ascii")
            # print("Got this msg:", data)
            return data
