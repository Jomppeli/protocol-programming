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
        responseHandler(msg)

def responseHandler(msg):
    try:
        msgs = msg.split("\n")
        method = msgs[0]
        body = msgs[1:]

        method = method.strip()
        method1 = "LISTR"
        method2 = "ADDR"
        method3 = "DONER"

        if method == method1:
            print("Tasks:")
            for task in body:
                print(task)

        elif method == method2:
            for line in body:
                print(line)

        elif method == method3:
            for line in body:
                print(line)
        
    except IndexError:
        pass

def exit_prog(si,f):
    print("Pressed ctrl+c")
    sys.exit(0)
    

try:
        
        signal.signal(signal.SIGINT, exit_prog)
        #read_data(s)
        while True:
            s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #serverAddr = input("Server address: ")
            #serverPort = input("Server port: ")
            serverAddr = "localhost"
            serverPort = 8888
            print(serverAddr,serverPort)
            inp = input("1. LIST\n2. ADD\n3. MARK AS DONE\n4. CLOSE\n: ")
            
            if inp == "1":
                s.connect((serverAddr,serverPort))
                method = "LIST"
                parameters = ""
                data = method+"\r\n"+parameters+"\n"
                data_setup(s,data)
                read_data(s)
                s.close()

            elif inp == "2":
                parameters = input("Name of the task: ")
                s.connect((serverAddr, serverPort))
                method = "ADD"
                data = method+"\r\n"+parameters+"\n"
                data_setup(s,data)
                read_data(s)
                s.close()

            elif inp == "3":
                parameters = input("Number of the task: ")
                s.connect((serverAddr, serverPort))
                method = "DONE"
                data = method+"\r\n"+str(parameters)+"\n"
                data_setup(s,data)
                read_data(s)
                s.close()
                
            elif inp == "4":
                break
              
except ConnectionRefusedError:
        print("Server is not receiving connections.")

except ConnectionResetError:
    print("Server is not receiving connections.")


