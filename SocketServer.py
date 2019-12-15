import socket
import sys
from threading import Thread
import pickle
from time import sleep


class SocketServer:

    def __init__(self, maxPlayer = 5, host = '127.0.0.1', port = '8888', maxBuffer = 4096):
        self.maxClient = maxPlayer
        self.host = host
        self.port = port
        self.maxBuffer = maxBuffer
        self.clientList = []
        self.isConnecting = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.commandDict = {}

    def startServer(self):
        self.server.bind((self.host, self.port))
        self.server.listen(self.maxClient)
        print('Running Server at {}'.format(self.host))
        Thread(target=self._connectionLoop).start()

    def _connectionLoop(self):
        while self.isConnecting:
            connection, address = self.server.accept()
            ip, port = str(address[0]), str(address[1])
            print('Connected With {} : {}'.format(ip, port))
            self.clientList.append({
                'ip' : ip,
                'port' : port,
                'connection' : connection
            })

    # stop accepting connections
    def closeConnection(self):
        self.isConnecting = False
        print('Connecting Stopped, {} connected'.format(len(self.clientList)))

    def endServer(self):
        self.server.close()
        sys.exit()

    # def client_thread(connection, ip, port, max_buffer_size = 5120):
    #     is_active = True
    #
    #     while is_active:
    #         client_input = receive_input(connection, max_buffer_size)
    #
    #         if "--QUIT--" in client_input:
    #             print("Client is requesting to quit")
    #             connection.close()
    #             print("Connection " + ip + ":" + port + " closed")
    #             is_active = False
    #         else:
    #             print("Processed result: {}".format(client_input))
    #             connection.sendall("-".encode("utf8"))

    # broadcast serialized obj to client
    def broadcast(self, obj):
        data = pickle.dumps(obj)
        for client in self.clientList:
            conn = client.get('connection')
            conn.sendall(data)
            print('sent to {}'.format(client.get('port')))

    # start listening to multiple ClientServers
    def startListening(self):
        for client in self.clientList:
            Thread(target=self._listenerThread, args=(client.get('connection'), client.get('port'))).start()

    def _listenerThread(self, clientConn, clientPort):
        is_active = True
        while is_active:
            data = self._receiveInput(clientConn)

            if data == 'QUIT':
                print("Client is requesting to quit")
                connection.close()
                print("Connection " + clientPort + " closed")
                is_active = False
            else:
                print("Data {} from {}".format(data, clientPort))
                self.commandDict[clientPort] = data

    def _receiveInput(self, conn):
        data = conn.recv(self.maxBuffer)
        decoded = pickle.loads(data)
        return decoded


    # def receive_input(connection, max_buffer_size):
    #     client_input = connection.recv(max_buffer_size)
    #     client_input_size = sys.getsizeof(client_input)
    #
    #     if client_input_size > max_buffer_size:
    #         print("The input size is greater than expected {}".format(client_input_size))
    #
    #     decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    #     result = process_input(decoded_input)
    #
    # return result

if __name__ == "__main__":
    server = SocketServer(maxPlayer = 5, host = '', port = 12397)
    server.startServer()
    input('Press Enter When Connection Done')
    server.closeConnection()
    mydata = []
    for i in range(40):
        mydata.append(list(range(40)))
    server.broadcast(mydata)
    server.startListening()
    input('Press Enter To End Server')
    server.endServer()
