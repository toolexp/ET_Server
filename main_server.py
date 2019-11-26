from Modules.Config.Connection import Connection
from Modules.Config.Data import verify_ip, verify_port

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65450        # Port to listen on (non-privileged ports are > 1023)

connection = Connection()
try:
    # Ask user for Socket info
    host = input('Insert ip address of the server to listen:\n')
    port = input('Insert the port number to listen on (>1023):\n')
    while True:
        clients = input('Insert maximum number of handled clients:\n')
        if clients.isdigit():
            break
        else:
            print('Inserted value is not recognized, retry\n')
    if verify_ip(host) and verify_port(port):   # Verify values inserted, if OK the set connection with inserted values
        connection.create_connection(host, int(port))
        print('Server set to listen with IP {} in PORT {}'.format(host, port))
    else:   # Otherwise set connection with default values
        connection.create_connection(HOST, PORT)
        print("Can't verify inserted values...")
        print('Server set to listen with IP {} in PORT {}'.format(HOST, str(PORT)))
    connection.listen_connections(int(clients))
    while True:
        connection.accept_connection()
except Exception as e:
    error = 'Error with the server: ' + str(e)
    print(error)
finally:
    print('Server is being disconnected...')
    connection.close_server_connection()
