import socket
import sys
from SocketTransport import *


class Client(Transport):
    def __init__(self, host="127.0.0.1", port=65432):
        super().__init__(host, port)
        
    def goHome(self):
        self.txSocket("gh")

    def movX(self, pos):
        self.txSocket("gx {}".format(pos))

    def movY(self, pos):
        self.txSocket("gy {}".format(pos))

    def goToAbs(self, x, y):
        self.txSocket("ga {} {}".format(x, y))

    def endSession(self):
        self.txSocket("End sesssion")

    def rxHandler(self, requestSocket, data):
        if self.isValid(data):
            print('Robot Position: ', data.decode("utf-8"))

    def txSocket(self, data):
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("Creating port {} at port {}".format(self.host, self.port))
        self.transport.connect((self.host, self.port))
        self.transport.sendall(bytes(data, 'utf-8'))
        recvBuffer = self.transport.recv(MAX_BUFFER_SIZE)
        self.rxHandler(requestSocket=None, data=recvBuffer)
        self.transport.close()

def printUsage():
    print("To move home : gh")
    print("To move x positions : gx <num> ex : gx 3")
    print("To move y positions : gy <num> ex : gy 3")
    print("To move to point in grid : ga <numx>,<numy>ex : ga 3,2")

if __name__ == "__main__":
    RobotCommander = Client()
    print("Start Session")
    print("Type h to view list of commands")
    while True:
        command = input("Type command \n")
        if command.lower() == "x":
            RobotCommander.endSession()
            sys.exit(0)
        elif command.lower() == "h":
            printUsage()
        else:
            s_command = command.split()
            if s_command[0] == "gh":
                RobotCommander.goHome()
            elif s_command[0] == "gx":
                RobotCommander.movX(int(s_command[1]))
            elif s_command[0] == "gy":
                RobotCommander.movY(int(s_command[1]))
            elif s_command[0] == "ga":
                XY = s_command[1].split(",")
                RobotCommander.goToAbs(int(XY[0]),int(XY[1]))
            else:
                print("Invalid command")

