import socket
import os
import sys
import signal

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

            recv_bytes = 0
            while recv_bytes < msg_len:
                    temp = client.recv(1024)
                    temp = temp.decode('ascii')
                    msg += temp
                    recv_bytes += len(msg)

            response_setup(msg)
            

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
            print("RESPONSE: %s"% data)

    def response_setup(msg):
        msgs = msg.split("\n")
        method = msgs[0]
        blength = msgs[1]
        parameter = msgs[2]
        body = msgs[3]

        method = method.strip()
        method1 = "LIST"
        method2 = "DOWNLOAD"
        if method == method1:
            print("REQUEST: %s\nBODYLENGTH: %s\nPARAMETER: %s\nBODY: %s" % (method,blength,parameter,body))

            
            files = os.listdir("files")
            
            for filename in files:
                body += filename + "\r\n"
            
            blength1 = len(body)
            data = method+"\r\n"+str(blength1)+"\r\n"+parameter+"\r\n"+body+"\n"
            data_setup(sock,data)
            
            
        elif method == method2:
            print("REQUEST: %s\nBODYLENGTH: %s\nPARAMETER: %s\nBODY: %s" % (method,blength,parameter,body))

            files = os.listdir("files")
            body = body.strip()
            if body in files:
                parameter1 = body
                f = open(("files/%s" %parameter1), "r")
                body1 = f.read()
                blength1 = len(body1)
                method1 = "SEND"

            elif body not in files:
                method1 = "ERROR"
                parameter1 = "File error"
                body1 = "File %s not found" % body
                blength1 = len(body1)
            
             
            data = method1+"\r\n"+str(blength1)+"\r\n"+parameter1+"\r\n"+body1+"\n"
            data_setup(sock,data)
        
    def exit_prog(si,f):
        print("Pressed ctrl+c")
        sys.exit(0)


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    sock.bind(("localhost", 8888))
    sock.listen(5)
    signal.signal(signal.SIGINT, exit_prog)
    while True:
        (client,addr)=sock.accept()
        print("Received a connection from",addr)
    
        read_data(sock,addr)
        client.close()
            
          

if __name__ == "__main__":
	main()
