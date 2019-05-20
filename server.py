import socket
import time
import pickle

#socket is endpoint that receives data

HEADERSIZE = 10

#AF_INET = IPV4
#SOCK_STREAM = TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#lockal host, portnumber can be any 4-digit number
s.bind((socket.gethostname(), 1234))
s.listen(5)

#listening forever
while True:
    #accepting everyone
    #storing socket object into clientsocket addres
    #address is their ip address
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    '''
    while True:
        time.sleep(3)
        msg = f"The time is! {time.time()}"
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        clientsocket.send(bytes(msg, "utf-8"))
     
    d = "Welcome to the server!"
    msg = pickle.dumps(d)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
    clientsocket.send(msg)
    '''   

    d = {1: "Hey", 2: "There"}
    msg = pickle.dumps(d)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
    clientsocket.send(msg)

    #closing by the end
    clientsocket.close()

