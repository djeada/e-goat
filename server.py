import socket

#socket is endpoint that receives data

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
    #sending data to whoever has connected
    clientsocket.send(bytes("Welcome to the server!", "utf-8"))
    #closing by the end
    clientsocket.close()
