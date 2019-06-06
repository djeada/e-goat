import socket
import select
import string

SIZE_OF_HEADER = 10

IP = "127.0.0.1"
PORT = 1234

#list of files supplied by clients
#append empty lists in first two indexes to make it 2D
files_list = [["" for _ in range(2)] for _ in range(100)]
index = 0

# Create a socket, constructor accepts two arguemtns
# first is address family (IPv4, IPv6, Blutooth or other) we want IPv4
# second is connection protocol (socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#some required configuration
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# binding informs OS that we will use a specific socket (we have to choose ip_address and port number)
server_socket.bind((IP, PORT))

# this makes server listen to new connections
server_socket.listen(1)

print(f'Listening for connections on {IP}:{PORT}...')

# list of sockets for select.select()
sockets_list = [server_socket]

# list of connected clients - socket as a key, user header and name as data
clients = {}

#this function is used to search trough the list of clients
def find(myList, v):
    for i, x in enumerate(myList):
        if v in x:
            return i

# Handles message receiving
def receive_message(client_socket):

    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket.recv(SIZE_OF_HEADER)

        # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())

        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
        # or just lost his connection
        # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
        # and that's also a cause when we receive an empty message
        return False

while True:

    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:

        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()

            # Client should send his name right away, receive it
            user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        # Else existing socket is sending a message
        else:

            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            #check if client is sending his files, if so add them to 
            if 'file' in message["data"].decode("utf-8"):
                user = clients[notified_socket]
                old_set = message["data"].decode("utf-8")
                new_set = old_set.replace('file', '')
                files_list[index][0] = new_set
                files_list[index][1] = user["data"].decode("utf-8")
                index = index + 1

            #check if client wants to download
            elif 'download' in message["data"].decode("utf-8"):
                user = clients[notified_socket]
                old_set = message["data"].decode("utf-8")
                new_set = old_set.replace('download ', '')

                pos = find(files_list, new_set)
                
                if pos is not None:
                    print(f'\n found at postion {files_list[pos][1]}\n')
                    
                    # Iterate over connected clients and broadcast message
                    for client_socket in clients:
                        # But don't sent it to sender
                        if client_socket != notified_socket:
                            new_mess = 'send ' + new_set
                            new_message = new_mess.encode('utf-8')
                            new_message_header = f"{len(new_message):<{SIZE_OF_HEADER}}".encode('utf-8')
                            client_socket.send(new_message_header + new_message)
                        #Sender gets special message recives after which he opens his ports
                        else:
                            new_mess2 = 'recive'
                            new_message = new_mess2.encode('utf-8')
                            new_message_header = f"{len(new_message):<{SIZE_OF_HEADER}}".encode('utf-8')
                            client_socket.send(new_message_header + new_message)
                            
                else:
                    print(f'\n FILE {new_set} WAS NOT FOUND \n')
                            
            elif 'show' in message["data"].decode("utf-8"):
                # Get user by notified socket, so we will know who sent the message
                user = clients[notified_socket]

                print(f'\nCurrent list of files: ')
                print(f'File_Name: \t\t Owner: ')
                
                printable_list = files_list[:index]
                print('\n'.join(map('\t\t '.join, printable_list)))

                print(f'\nReceived message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
                      
    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]


