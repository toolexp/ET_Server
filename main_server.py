from Modules.Config.Connection import Connection
from Modules.Config.protocol import handle_decision
from Modules.Config.Data import verify_ip, verify_port

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65450        # Port to listen on (non-privileged ports are > 1023)
HEADER_SIZE = 10    # Length that indicates the number of characters in the received message

connection = Connection()
try:
    # Ask user for Socket info
    host = input('Insert ip address of the server to listen:\n')
    port = input('Inset the port number to listen on (>1023):\n')
    if verify_ip(host) and verify_port(port):   # Verify values inserted, if OK the set connection with inserted values
        connection.create_connection(host, int(port))
        print('Server set to listen with IP {} in PORT {}'.format(host,port))
    else:   # Otherwise set connection with default values
        connection.create_connection(HOST, PORT)
        print("Can't verify inserted values...")
        print('Server set to listen with IP {} in PORT {}'.format(HOST, str(PORT)))
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
    connection.close_connection()
except Exception as e:
    error = 'Error with the server: ' + str(e)
    print(error)
finally:
    connection.close_connection()
