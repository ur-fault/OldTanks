import socket, random, pickle, time
from _thread import start_new_thread, error


class IP:
    def __init__(self):
        self.get_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_ip.connect(("8.8.8.8", 80))
        print("Write this IP to other computers: " + self.get_ip.getsockname()[0])
        self.server = self.get_ip.getsockname()[0]
        self.get_ip.close()


class connection:
    def __init__(self, conn, my_pos, order, main):
        self.conn = conn
        self.my_pos = my_pos
        self.order = [my_pos] + order
        self.bytes = 2048

        self.main = main
        self.main_loop()

    def main_loop(self):
        self.conn.send(pickle.dumps(self.order))
        print("Sent default data", str(self.order))

        _wait = True
        while self.main.count_now < self.main.count:
            # print("Sent wait post")
            # self.conn.send("Wait".encode("ascii"))
            # print("Waiting")
            pass

        time.sleep(0.1)

        run = True
        while run:
            data_to_send = self.conn.recv(self.bytes)
            if self.my_pos == -1:
                print("Recv", str(data_to_send))
            self.main.send_to_all(data_to_send, self)


class Main:
    def __init__(self):
        self.get_ip = IP()
        self.server = self.get_ip.server
        self.port = 5555
        self.addr = (self.server, self.port)
        self.count = self.get_count_conn()
        print(self.count)
        self.count_now = 0
        self.order = self.get_order()
        self.conns = []

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            str(e)
        self.s.listen(1)
        self.listen()

    def get_count_conn(self):
        while True:
            count = 0
            try:
                count = int(input("Type expected number of connections (max 4 and min 1): "))
            except OSError as e:
                print(e)
                pass

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

    def listen(self):
        listening = True
        pos = 0
        while listening:
            if len(self.conns) < self.count:
                conn, addr = self.s.accept()
                self.count_now += 1
                print("Connected to:", addr)
                start_new_thread(connection, (conn, pos, self.order, self))
                self.conns.append(conn)
                pos += 1

    def send_to_all(self, msg, sender):
        for conn in self.conns:
            if conn != sender.conn:
                conn.send(msg)
                if sender.my_pos == -1:
                    print("Sent", msg)


m = Main()
