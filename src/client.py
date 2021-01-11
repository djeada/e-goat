# client.py  
import socket

MAX_BYTES = 1024

def start_client(host = socket.gethostname(), port = 9999):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	client_socket.connect((host, port))
	return client_socket

def run_client(client):
	tm = client.recv(MAX_BYTES)
	recive_file(client)                                  
	client.close()
	print("The time got from the server is %s" % tm.decode('ascii'))

def recive_file(conn, file_name='recived_file.jpeg'):
	with open(file_name, 'wb') as f:
		while True:
			data = conn.recv(MAX_BYTES)
			if not data:
				break
			f.write(data)


client_socket = start_client()
run_client(client_socket)
