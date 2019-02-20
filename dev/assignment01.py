import socket

def send_data(socket,data):
	total = 0
	while total < len(data):
		sent = socket.send(data.encode('ascii')[total:])
		total= total + sent
	print("Sent %d bytes" % (total))

def data_setup(socket,data):
	data_len = len(data)
	send_data(socket, str(data_len)+'\n')
	send_data(socket,data)

def recv_data_setup(s):
		data_len = ''
		while True:
			temp = s.recv(1)
			temp = temp.decode('ascii')
			if temp == '\n':
				break
			data_len = data_len +  temp
		return(int(data_len))

def read_data(s):
	msg = ''
	msg_len = recv_data_setup(s)
	print("Bytes incoming: %d" % msg_len)

	recv_bytes = 0
	while recv_bytes < msg_len:
		temp = s.recv(1024)
		temp = temp.decode('ascii')
		msg += temp
		recv_bytes += len(msg)
	print("Received bytes: %d" % recv_bytes)
	print("Message from server:\n%s" % (msg))

data = "Morjesta boy. Is anyone there?"

try:
	s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("localhost",8888))
	data_setup(s,data)
except ConnectionRefusedError:
	print("Server is not receiving connections.")
except NameError:
	print("Data is not defined.")
read_data(s)

s.close()
