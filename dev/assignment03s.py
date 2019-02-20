import socket

def main():

	def recv_data_setup(socket):
		data_len = ''
		while True:
			temp = client.recv(1)
			temp = temp.decode('ascii')
			if temp == '\n':
				break
			data_len = data_len +  temp
		return(int(data_len))

	def read_data(socket,addr):
		msg = ''
		addr = addr[0]
		msg_len = recv_data_setup(socket)
		print("Bytes incoming: %d" % msg_len)

		recv_bytes = 0
		while recv_bytes < msg_len:
			temp = client.recv(1024)
			temp = temp.decode('ascii')
			msg += temp
			recv_bytes += len(msg)
		print("Received bytes: %d" % recv_bytes)
		print("Message from %s:\n%s" % (addr,msg))

	def send_data(socket,data):
		total = 0
		while total < len(data):
			sent = client.send(data.encode('ascii')[total:])
			total= total + sent
		print("Sent %d bytes" % (total))

	def data_setup(socket,data):
		data_len = len(data)
		send_data(socket, str(data_len)+'\n')
		send_data(socket,data)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

	while True:
		print("Enter the address: ")
		address = input()
		print("Enter the port:  ")
		port = int(input())
		if any([address == '', port == '']):
			print("Please enter the values.")
			exit()
		else:
			print("Good job.")
			sock.bind((address, port))
			break
	
	
	
	while True:
		sock.listen(5)
		(client,addr)=sock.accept()
		while True:
			print("Received a connection from",addr)
			data_to_client = "Hello and welcome."
			data_setup(sock,data_to_client)
			read_data(sock,addr)
			break


if __name__ == "__main__":
	main()
