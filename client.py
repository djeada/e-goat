import socket

#socket is endpoint that receives data

#AF_INET = IPV4
#SOCK_STREAM = TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#lockal host, portnumber can be any 4-digit number
s.connect((socket.gethostname(), 1234))

full_msg = ''

#accept the message that was send to us from the server
while True:
    msg = s.recv(8)  
    if len(msg) <= 0:
        break
    full_msg += msg.decode("utf-8")
    
print(full_msg)
