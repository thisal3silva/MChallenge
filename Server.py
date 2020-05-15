from SocketTransport import Transport
import socket
import sys

class Server(Transport):
    def __init__(self, host="127.0.0.1", port=65432):
        super().__init__(host, port)
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen()
        self.X =1
        self.Y =1

    def moveX(self, pos):
        if self.X + pos > 0:
            self.X += pos

    def moveY(self, pos):
        if self.Y + pos > 0:
            self.Y += pos

    def moveToPos(self, x, y):
        if x > 0:
            self.X = x
        if y > 0:
            self.Y = y

    def getPosString(self):
        return "{},{}".format(self.X, self.Y)

    def rxHandler(self,requestSocket, data):
        data = data.decode("utf-8")
        print('Received ', data)
        if data == "End sesssion":
            self.close()
            sys.exit(0)
        else:
            s_data = data.split()

            if data == "gh":
                self.moveToPos(1,1)
                requestSocket.sendall(self.str2Bytes(self.getPosString()))

            if s_data[0] == "ga":
                self.moveToPos(int(s_data[1]),int(s_data[2]))
                requestSocket.sendall(self.str2Bytes(self.getPosString()))

            elif s_data[0] == "gx":
                self.moveX(int(s_data[1]))
                requestSocket.sendall(self.str2Bytes(self.getPosString()))

            elif s_data[0] == "gy":
                self.moveY(int(s_data[1]))
                requestSocket.sendall(self.str2Bytes(self.getPosString()))

            else:
                requestSocket.sendall(b"Invalid command")

RobotManipulator = Server()

while True:
    RobotManipulator.acceptConnection()


