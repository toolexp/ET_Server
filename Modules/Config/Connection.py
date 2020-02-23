"""
File where all functions associated with the connection (client-server) are defined: create and close connection,
compose, decompose, receive and send messages, and handle clients with threads
"""

from socket import socket, AF_INET, SOCK_STREAM
from pickle import dumps, loads
from _thread import start_new_thread
from Modules.Config.protocol import handle_decision

HEADER_SIZE = 10  # Length that indicates the number of characters in the stream


def client_thread(current_client, address, port):
    """
    Thread that handles an specific client. Here is the main loop where each client is treated with the server. In this
    function the server exchanges information with each client.

    :param current_client: client socket from which the server is receiving the message
    :type current_client: socket.socket
    :param address: IP address of client from which the server is receiving the message
    :type address: str
    :param port: port number of client from which the server is receiving the message
    :type port: int
    """
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
    """
    Sends the message represented as a stream of bytes to a client, which is identified vy the current client socket

    :param current_client: client socket from which the server is receiving the message
    :type current_client: socket.socket
    :param stream: stream of bytes that the server wants to send to the client
    :type stream: bytes
    """
    current_client.sendall(stream)


def receive_message(current_client, address, port):
    """
    Receives a stream of bytes from a client. First, the function reads the first HEADER_SIZE bytes to know the
    actual length of the payload. With that, the function starts to receive al received streams, until it reaches the
    length. After that, the received stream is reconstructed and converted to a Message object, so the server is
    is capable of reading it

    :param current_client: client socket from which the server is receiving the message
    :type current_client: socket.socket
    :param address: IP address of client from which the server is receiving the message
    :type address: str
    :param port: port number of client from which the server is receiving the message
    :type port: int
    :return message: message reconstructed from the stream of bytes
    :rtype message: Modules.Config.Data.Message
    """
    new_msg = True
    header_ctrl = True
    stream = b''
    msg_len = 0
    while new_msg:
        msg = current_client.recv(20)
        if header_ctrl:
            msg_len = int(msg[:HEADER_SIZE].decode('utf-8'))
            print('Client {}:{} sent stream of length: {}'.format(address, port, msg_len))
            header_ctrl = False

        stream += msg
        if len(stream) - HEADER_SIZE == msg_len:
            print('Full message received')
            message = loads(stream[HEADER_SIZE:])
            return message


def create_message(data):
    """
    Creates a bytes flow from the message that the server has fulfilled already. Here the the stream of bytes is
    created from the message itself, so it can be sent to the client through the network. The stream contains two
    parts: header and data, where header is a number that represents the length of the data (this field is of
    HEADER_SIZE bytes), and data is the actual payload (stream of the message)

    :param data: message that the server wants to send to a client
    :type data: Modules.Config.Data.Message
    :return stream: stream of bytes conatining the message
    :rtype stream: bytes
    """
    message = data
    body = dumps(message)
    header = '{:<{}}'.format(len(body), HEADER_SIZE)
    stream = bytes(header, 'utf-8') + body
    return stream


class Connection:
    """
    A class used to represent a connection of server with clients. A connection object has attributes:

    :param c_socket: a socket object from which the client is connected to the server
    :type c_socket: socket.socket
    """

    def __init__(self, c_socket=socket(AF_INET, SOCK_STREAM)):
        """
        Constructor of the class. It creates a socket objetct

        :param c_socket: a socket object
        :type c_socket: socket.socket
        """
        self.c_socket = c_socket

    def create_connection(self, host, port):
        """
        Establishes a socket endpoint with an IP address and a port number, so the server can listen to connections

        :param host: IP address of the server where it will be listening to client connections
        :type host: str
        :param port: port number for the establishment of the server socket
        :type port: int
        """
        self.c_socket.bind((host, port))

    def listen_connections(self, max):
        """
        Makes server available to accept new connections from clients

        :param max: number of client connections that the server will be allowed to accept
        :type max: int
        """
        self.c_socket.listen(max)

    def accept_connection(self):
        """
        Accepts a connection request from a client and send it to a thread so it can be handled by the server
        as other clients
        """
        conn, addr = self.c_socket.accept()
        print('Connected with {}:{}'.format(addr[0], addr[1]))
        start_new_thread(client_thread, (conn, addr[0], addr[1],))

    def close_server_connection(self):
        """
        Close connection of the socket with all its clients and stops listening for new connections
        """
        self.c_socket.close()