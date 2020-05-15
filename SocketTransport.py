import socket
MAX_BUFFER_SIZE = 1024

class Transport:
    def __init__(self, host="127.0.0.1", port=65432):
        self.host=host
        self.port=port
        self.status = True
        self.transport = None

    def str2Bytes(self,data):
        return bytes(data,'utf-8')

    def isValid(self, data):
        if not data:
            return False
        else:
            return True

    def listen(self):
        self.transport.bind((self.host, self.port))
        self.transport.listen()
        print('Listening on', (self.host, self.port))

    def acceptConnection(self):
        requestSocket, address = self.transport.accept()
        with requestSocket:
            #print("Connected to {}".format(address))
            data = requestSocket.recv(MAX_BUFFER_SIZE)
            if self.isValid(data):
                self.rxHandler(requestSocket,data)

    def close(self):
        print("End Session")

    def rxHandler(self, requestSocket, data):
        print('Received', repr(data))
        if requestSocket is not None:
            requestSocket.sendall(data)