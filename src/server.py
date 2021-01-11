import socket                                         
import time
from pathlib import Path
from threading import Thread
from SocketServer import ThreadingMixIn

MAX_REQUESTS = 5
MAX_BYTES = 1024

#host default local machine
def start_server(host = socket.gethostname(), port = 9999):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                           
	server_socket.bind((host, port))                                  
	server_socket.listen(MAX_REQUESTS)
	return server_socket

def run_server(server):
	while True:
		conn, addr = server.accept()
		print("Got a connection from %s" % str(addr))
		currentTime = time.ctime(time.time()) + "\r\n"
		#must be encoded Python by default uses unicode
		conn.send(currentTime.encode('ascii'))
		send_file(conn, "0.jpeg")
		conn.close()

def send_file(conn, file_name):
	f = open(file_name,'rb')
	l = f.read(Path(file_name).stat().st_size)
	while (l):
		conn.send(l)
		l = f.read(MAX_BYTES)
		f.close()


server = start_server()
run_server(server)
