import socket
import select
import errno
import sys
from os import listdir
from os.path import isfile, join

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")
mypath = 'C:\\Users\\Adam\\Desktop\\ChatServer'

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

#Send list of your files
files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for f in files:
    message = 'file'
    message += f
    
    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
    message = message.encode('utf-8')
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)
     
while True:
    
    # Wait for user to input a message
    message = input(f'{my_username} > ')

    # If message is not empty - send it
    if message:

        # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print('{message}')
            
            if 'send' in message:
                print('hallo')
                new_port = 5000                # Reserve a port for your service every new transfer wants a new port or you must wait.
                s = socket.socket()             # Create a socket object
                s.bind((IP, new_port))          # Bind to the port
                s.listen(5)                     # Now wait for client connection.
                
                while True:
                    conn, addr = s.accept()     # Establish connection with another client.
                    data = conn.recv(1024)
                    print('Server received', repr(data))

                    old_set = message["data"].decode("utf-8")
                    filename = old_set.replace('send ', '')
                    f = open(filename,'rb')
                    l = f.read(1024)
                    while (l):
                       conn.send(l)
                       print('Sent ',repr(l))
                       l = f.read(1024)
                    f.close()
                    conn.close()
            elif 'recive' in message:
                s = socket.socket()             # Create a socket object
                new_port = 5000                    # Reserve a port for your service every new transfer wants a new port or you must wait.

                s.connect((IP, new_port))

                with open('received_file', 'wb') as f:
                    while True:
                        print('receiving data...')
                        data = s.recv(1024)
                        print('data=%s', (data))
                        if not data:
                            break
                        # write data to a file
                        f.write(data)
                f.close()
                s.close()

    #exception handling
    except IOError as errorino:
        if errorino.errno != errno.EAGAIN and errorino.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(errorino)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as errorino:
        # If something unexpected happended escape 
        print('WARNING CRITICAL ERROR: '.format(str(errorino)))
        sys.exit()
