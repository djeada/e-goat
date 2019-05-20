import socket
import pickle 

#socket is endpoint that receives data

HEADERSIZE = 10

#AF_INET = IPV4
#SOCK_STREAM = TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#lockal host, portnumber can be any 4-digit number
s.connect((socket.gethostname(), 1234))


#accept the message that was send to us from the server
while True: 

    #buffers for data stream
    full_msg = b''
    new_msg = True

    while True: 
        msg = s.recv(16)  
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg
        
        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)

            #clear the buffers
            full_msg = b''
            new_msg = True
    
print(full_msg)


