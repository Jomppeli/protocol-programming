import socket
import signal
import sys

def send_data(socket,data):
        total = 0
        while total < len(data):
                sent = socket.send(data.encode('ascii')[total:])
                total= total + sent
        

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

        recv_bytes = 0
        while recv_bytes < msg_len:
                temp = s.recv(1024)
                temp = temp.decode('ascii')
                msg += temp
                recv_bytes += len(msg)
        jeppis(msg)

def jeppis(msg):
    try:
        msgs = msg.split("\n")
        method = msgs[0]
        blength = msgs[1]
        parameter = msgs[2]
        body = msgs[3:]

        method = method.strip()
        method1 = "LIST"
        method2 = "SEND"
        method3 = "ERROR"

        if method == method2:
            receive_file(blength,parameter,body)

        elif method == method1:
            list_files(body)

        elif method == method3:
            for line in body:
                print(line)
        
    except IndexError:
        pass

def receive_file(blength,parameter,body):
    parameter = parameter.strip()
    filename = parameter
    f = open(filename, "w")
    for line in body:
        f.write(line + "\n")
    f.close()
    print("File %s downloaded!" % filename)
            

def list_files(body):
    print("Files in the server:")
    for file in body:
        print(file)

def exit_prog(si,f):
    print("Pressed ctrl+c")
    sys.exit(0)
    

try:
        
        signal.signal(signal.SIGINT, exit_prog)
        #read_data(s)
        while True:
            s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            inp = input("1. LIST\n2. DOWNLOAD\n3. CLOSE\n: ")
            
            if inp == "1":
                s.connect(("localhost",8888))
                method = "LIST"
                parameters = "files"
                body = ""
                blength = len(body)
                data = method+"\r\n"+str(blength)+"\r\n"+parameters+"\r\n"+body+"\n"
                data_setup(s,data)
                read_data(s)
                s.close()

            elif inp == "2":
                body = input("FILENAME: ")
                s.connect(("localhost",8888))
                method = "DOWNLOAD"
                parameters = "files"
                blength = len(body)
                data = method+"\r\n"+str(blength)+"\r\n"+parameters+"\r\n"+body+"\n"
                data_setup(s,data)
                read_data(s)
                s.close()
            
            elif inp == "3":
                break
              
except ConnectionRefusedError:
        print("Server is not receiving connections.")

except ConnectionResetError:
    print("Server is not receiving connections.")


