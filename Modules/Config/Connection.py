from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from _thread import start_new_thread
from Modules.Config.protocol import handle_decision

HEADER_SIZE = 10  # Length that indicates the number of characters in the stream


def client_thread(current_client, address, port):
    while True:
        message = receive_message(current_client, address, port)
        if message.comment == 'close_connection':
            current_client.close()
            print('Connection closed by the client {}:{}'.format(address, port))
            break
        msg_rspt = handle_decision(message)
        stream = create_message(msg_rspt)
        send_message(current_client, stream)


def send_message(current_client, stream):
    current_client.sendall(stream)


def receive_message(current_client, address, port):
    new_msg = True
    header_ctrl = True
    stream = b''
    while new_msg:
        msg = current_client.recv(20)
        if header_ctrl:
            msg_len = int(msg[:HEADER_SIZE].decode('utf-8'))
            print('Client {}:{} sent stream of length: {}'.format(address, port, msg_len))
            header_ctrl = False

        stream += msg
        if len(stream) - HEADER_SIZE == msg_len:
            print('Full message received')
            #new_msg = False
            #header_ctrl = True
            message = loads(stream[HEADER_SIZE:])
            return message


def create_message(data):
    message = data
    body = dumps(message)
    header = '{:<{}}'.format(len(body), HEADER_SIZE)
    stream = bytes(header, 'utf-8') + body
    return stream


class Connection():

    def __init__(self, c_socket=socket(AF_INET, SOCK_STREAM)):
        self.c_socket = c_socket

    def create_connection(self, host, port):
        self.c_socket.bind((host, port))

    def listen_connections(self, max):
        self.c_socket.listen(max)

    def accept_connection(self):
        conn, addr = self.c_socket.accept()
        print('Connected with {}:{}'.format(addr[0], addr[1]))
        start_new_thread(client_thread, (conn, addr[0], addr[1],))

    def close_server_connection(self):
        self.c_socket.close()