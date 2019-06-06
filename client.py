import socket
import select
import errno
import sys
import time
import threading
from os import listdir
from os.path import isfile, join

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
NEW_PORT = 3000
my_username = input("Username: ")
mypath = 'C:\\Users\\Adam\\Desktop\\ChatServer'

def clientthread(filename):
    result = None
    while result is None:
        try:
            s = socket.socket()
            s.connect((IP, NEW_PORT))

            with open('received_file', 'wb') as f:
                while True:
                    print('receiving data...')
                    data = s.recv(1024)
                    result = data
                    print('data=%s', (data))
                    if not data:
                        break
                    # write data to a file
                    f.write(data)
            f.close()
            s.close()
        except:
            pass
 
def serverthread(filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP, NEW_PORT))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        f = open(filename,'rb')
        l = f.read(1024)
        while (l):
            conn.send(l)
            print('Sent ',repr(l))
            l = f.read(1024)
        f.close()
        conn.close()

if __name__ == "__main__":
    # Create a socket, constructor accepts two arguemtns
    # first is address family (IPv4, IPv6, Blutooth or other) we want IPv4
    # second is connection protocol (socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
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
            # now we want to loop over received messages (there might be more than one) 
            while True:
            
                # receive our "header" containing message length, it's size is defined and constant
                message_header = client_socket.recv(HEADER_LENGTH)

                # if message is empty we close connection socket.close() or socket.shutdown(socket.SHUT_RDWR)
                if not len(message_header):
                    print('Connection closed by the server')
                    sys.exit()

                # convert header to int value
                message_length = int(message_header.decode('utf-8').strip())

                recived_message = client_socket.recv(message_length).decode('utf-8')

                # create small server socket for handling file transfer
                if 'send' in recived_message:
                    old_set = message["data"].decode("utf-8")
                    filename = old_set.replace('send ', '')

                    try:
                        print(f'hallo in Server')
                        x = threading.Thread(target=serverthread, args=(filename,))
                        x.start()
                    except:
                        print (f'Error: unable to start thread')
                
                # create small client socket for handling file transfer
                elif 'recive' in recived_message:
                    try:
                        print(f'hallo in Client')
                        filename = 'blabla'
                        x = threading.Thread(target=clientthread, args=(filename,))
                        x.start()
                    except:
                        print (f'Error: unable to start thread')
                
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
