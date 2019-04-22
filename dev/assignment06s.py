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

    def read_data(socket,addr,serverFile):
        # Go over the received data
        msg = ''
        addr = addr[0]
        msg_len = recv_data_setup(socket)

        recv_bytes = 0
        while recv_bytes < msg_len:
                temp = client.recv(1024)
                temp = temp.decode('ascii')
                msg += temp
                recv_bytes += len(msg)

        requestHandler(msg,serverFile)
            
    def data_setup(socket,data):
            data_len = len(data)
            send_data(socket, str(data_len)+'\n')
            send_data(socket,data)
            # Print the response that has been sent
            print("RESPONSE: %s"% data)

    def send_data(socket,data):
            total = 0
            while total < len(data):
                    sent = client.send(data.encode('ascii')[total:])
                    total= total + sent
            print("Sent %d bytes" % (total))

    def requestHandler(msg,serverFile):
        # Handle the request from the client. Split the message and handle it by the request method.
        
        msgSplit = msg.split("\n")
        # The message structure is: REQUEST PARAMETER
        clientRequest = msgSplit[0]
        clientRequest = clientRequest.strip()
        # The request can be LIST, DONE, ADD
        # The parameters are:
        # LIST: none
        # DONE: the number of the task (e.g 3)
        # ADD: the name of the task (e.g "Buy a car")
        
        request1 = "LIST"
        request2 = "DONE"
        request3 = "ADD"
        
        if clientRequest == request1:
            # LIST the TODO's from the file that was given as a command line argument
            # Send the data to the client as a LISTR response where the data is in the body
            print("TODO's:")
            f = open(serverFile,"r")
            fileContent = f.read()
            print(fileContent)

            body = fileContent
            data = "LISTR"+"\r\n"+body+"\n"
            data_setup(sock,data)
            
        elif clientRequest == request2:
            # Go over the todo's and if the task number doesn't match the number that the client wants to be removed,
            # write the task to the new file. So the task is not removed per say, it simply isn't just added to the newest version of the file.
            clientParameter = msgSplit[1]
            f = open(serverFile, "r")
            fileContent = f.readlines()
            f1 = open(serverFile, "w")
            print(clientParameter)
            taskNumber = 1
            for line in fileContent:
                split = line.split(")")
                if split[0] != clientParameter:
                    line = "%d)%s" % (taskNumber,split[1])
                    f1.write(line)
                    taskNumber += 1

            # Send a success message to the client as a DONER response
            
            body = "Task deleted."
            data = "DONER"+"\r\n"+body+"\n"
            data_setup(sock,data)

        elif clientRequest == request3:
            # Take the task and add a number in front of it and append it to the file
            # Go over the file and count the lines(tasks) and number the newest task accordingly
            clientParameter = msgSplit[1]
            print(clientParameter)
            f0 = open(serverFile, "r")
            fileContent = f0.readlines()
            f0.close()
            taskNumber = 1
            for line in fileContent:
                taskNumber += 1
            task = "\n%d) %s" % (taskNumber,clientParameter)
            f1 = open(serverFile, "a")
            f1.write(task)
            f1.close()

            # Send a success messge to the client as a ADDR response
            body = "Task %s added!" % clientParameter
            data = "ADDR"+"\r\n"+body+"\n"
            data_setup(sock,data)
            
        

    def claHandler():
        # Handles the command line arguments
        # Checks that the address is valid (either "localhost" or contains 3 dots.)
        # Checks that the port number has 4 digits
        # Checks that the given filename is a .txt file
        # If the extension is something else, exit the program
        # If there is no given extension, try to add a .txt and see if any files exists. So it isn't necessary to put the .txt after the filename.
        # If the file doesn't exist, create it
        try:
            serverAddr = sys.argv[1]
            serverPort = sys.argv[2]
            serverFile = sys.argv[3]

            serverAddr = serverAddr.strip()
            if serverAddr == "localhost":
                pass
            elif serverAddr.count(".") == 3:
                pass
            else:
                print("Invalid address.")
                sys.exit()

            if len(serverPort) == 4:
                pass
            else:
                print("Invalid port.")
                sys.exit()
            
            try:
                fileExt = serverFile.split(".")
                fileExt = fileExt[1]
                if fileExt != "txt":
                    print("Filename invalid. Only .txt files can be used.")
                    sys.exit()
                else:
                    pass
            except IndexError:
                serverFile += ".txt"

            print(serverAddr, serverPort, serverFile)

            # Try to open the file, if it doesn't exist, ask the user if he wants to create the file, or was it just a typo
            try:
                f = open(serverFile, "r")

            except FileNotFoundError:
                userInput = input("File not found. Create a file called %s? Y/N: " % serverFile)
                if userInput == "y" or userInput == "Y":
                    f = open(serverFile, "w+")
                    print("File created.")
                    
                    
                elif userInput == "n" or userInput == "N":
                    print("File not created. Exiting.")
                    sys.exit()
            
        except IndexError:
            print("Check the command line arguments and try again.\n\
                python3 assignment06s.py <address> <port> <filename>")
            sys.exit()

        return(serverAddr,serverPort,serverFile)
            
    # Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

    # Get the command line arguments
    serverAddr,serverPort,serverFile = claHandler()

    print("Listening on: %s:%s\nFilename: %s" % (serverAddr,serverPort,serverFile))
    
    sock.bind((serverAddr, int(serverPort)))
    sock.listen(5)
    
    while True:
        (client,addr)=sock.accept()
        print("Received a connection from",addr)
        while True:
            read_data(sock,addr,serverFile)
            break

    
          

if __name__ == "__main__":
	main()
