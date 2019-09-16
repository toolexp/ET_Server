from Modules.Config.Connection import Connection
from Modules.Config.protocol import handle_decision

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65450        # Port to listen on (non-privileged ports are > 1023)
HEADER_SIZE = 10    # Length that indicates the number of characters in the received message

connection = Connection()
if True:
    connection.create_connection(HOST, PORT)
    connection.listen_connections(5)
    connection.accept_connection()
    while True:
        connection.receive_message()
        if connection.message.comment == 'close_connection':
            connection.close_connection()
            print('Connection closed by the client')
            break
        msg_rspt = handle_decision(connection)
        connection.create_message(msg_rspt)
        connection.send_message()
'''except Exception as e:
    error = 'Error with the server: ' + str(e)
    print(error)
finally:
    connection.close_connection()'''
