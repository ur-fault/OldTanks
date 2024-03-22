import socket
from _thread import start_new_thread, error
import random
import sys
import time
import pickle


get_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
get_ip.connect(("8.8.8.8", 80))
print("Write this IP to other computers: " + get_ip.getsockname()[0])
server = get_ip.getsockname()[0]
port = 5555

count = 0
msg_data = [0]
order = []
this_conn = 0
connected = 0
has_sent_msg = 0
msg_num = 0
_first_data_was_sent = False
call = []
reply = []
bytes = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

while True:
    try:
        count = int(input("Type expected number of connections (max 4 and min 1): "))
    except: pass

    if 5 > count > 0:
        break


for x in range(count):
    while True:
        this_order = random.randint(0, 3)
        if not this_order in order:
            order.append(this_order)
            break

print(order)

s.listen(count)
print("Waiting for connection, Server started")


def threaded_client(this_connection, order, full_order, conn_num):
    _wait = True
    _wait2 = True
    global connected
    global this_conn
    global msg_data
    global has_sent_msg

    this_conn += 1
    connected += 1
    print("[{}]".format(conn_num), connected, "/", count)
    this_connection.sendall(str(order).encode("ascii"))
    this_connection.sendall(pickle.dumps(full_order))
    print("[{}]".format(conn_num), "Sent Order of all players: " + str(full_order))
    data = pickle.loads(this_connection.recv(bytes))
    print("[{}]".format(conn_num), "Recieved " + str(data))

    msg_data.append(data)
    print("[{}]".format(conn_num), "Data now looks like:", str(msg_data))

    while _wait2:
        if len(msg_data) >= count:
            _wait2 = False
    _wait2 = True
    print("Go to the main fun")

    while _wait:
        if connected >= count:
            _wait = False
            print("[{}]".format(conn_num), "All players are connected")
            this_connection.send(pickle.dumps(msg_data))
            has_sent_msg += 1
            print("[{}]".format(conn_num), "Sent some data:", msg_data)
            while has_sent_msg < connected:
                print("[{}]".format(conn_num), "Waiting for clear")
                time.sleep(1)
            msg_data = [msg_num]
            time.sleep(0.1)
            has_sent_msg = 0
            while True:
                try:
                    time.sleep(1)
                    data = pickle.loads(this_connection.recv(bytes))
                    print("[{}]".format(conn_num), "Recv:", str(data))
                    # print("Recv:", data)
                    msg_data.append(data)
                    # print("Have data from:", len(some_data)
                    print("[{}]".format(conn_num), "Have data from:", len(msg_data))

                    while len(msg_data) < count + 1:
                        print("[{}]".format(conn_num), "Have data from:", len(msg_data) - 1)
                        time.sleep(1)
                    _wait2 = True
                    print("[{}]".format(conn_num), "Sent", str(msg_data))
                    this_connection.send(pickle.dumps(msg_data))
                    has_sent_msg += 1
                    while has_sent_msg < connected:
                        time.sleep(1)
                        pass
                    print("[{}]".format(conn_num), "Clearing msg data")
                    msg_data = [msg_num]
                    has_sent_msg = 0

                    if not data:
                        print("Disconnected")
                        break

                except error as e:
                    print(e)
                    break

            print("Lost connection")
            connected -= 1
            this_conn -= 1
            this_connection.close()
        elif connected + 1 < count:
            print("Waiting for other players")


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn, order[this_conn % count], order, this_conn))
    # print(some_data)

import socket, time, pickle, random

class getIP:
    def __init__(self):
        self.get_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_ip.connect(("8.8.8.8", 80))
        print("Write this IP to other computers: " + self.get_ip.getsockname()[0])
        self.server = self.get_ip.getsockname()[0]
        self.port = 5555

class conn:
    def __init__(self):



class server:
    def __init__(self):
        get_ip = getIP()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = get_ip.server
        self.port = get_ip.port
        self.count = self.get_count_conn()
        self.order = self.get_order()

        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)

    def get_count_conn(self):
        while True:
            count = 0
            try:
                count = int(input("Type expected number of connections (max 4 and min 1): "))
            except: pass

            if 5 > count > 0:
                return count

    def get_order(self):
        order = []
        for x in range(self.count):
            while True:
                this_order = random.randint(0, 3)
                if not this_order in order:
                    order.append(this_order)
                    break

        print(order)
        return order

    s.listen(count)
    print("Waiting for connection, Server started")
