import socket
import sys
import pickle


class ClientServer:

    def __init__(self, host = '127.0.0.1', port = 8888, maxBuffer = 4096):
        self.host = host
        self.port = port
        self.maxBuffer = maxBuffer
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def startServer(self):
        self.server.connect((self.host, self.port))

    def receiveInput(self):
        data = self.server.recv(self.maxBuffer)
        decoded = pickle.loads(data)
        return decoded

    # broad cast to server only
    def broadcast(self, obj):
        data = pickle.dumps(obj)
        self.server.sendall(data)

if __name__ == "__main__":
    hostname = input('Host Name: ')
    server = ClientServer(host = hostname, port = 12397)
    server.startServer()
    print(server.receiveInput())
    # server.broadcast('hihihi')
    while True:
        a = input('Enter to Send')
        if a == 'q':
            break
        server.broadcast(a)
    input('Enter to Quit')
    server.broadcast('QUIT')
