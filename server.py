# Importing necessary libraries
import socket, os
from threading import Thread
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Declaring the global variables
IP_ADDRESS = '127.0.0.1'
PORT = 8000
SERVER = None
BUFFER_SIZE = 4096

# Creating an empty clients dictionary
clients = {}

# Checking the existence of the folder named "shared_files"
if not os.path.exists("shared_files"):
    os.makedirs("shared_files")

# Function to handle the client
def handleClient(client, name):
    global clients

    # Running an infinite loop to receive incoming messages from the client
    while True:
        try:
            # Receiving the message from the client
            message = client.recv(BUFFER_SIZE).decode()

            # Splitting the message to get the command and the data
            command, data = message.split("|")

            # Checking the command type
            if command == "CONNECT":
                clients[name]["connected_with"] = data
                clients[data]["connected_with"] = name

            elif command == "SEND":
                clients[clients[name]["connected_with"]]["client"].send(f"{name}|{data}".encode())

            elif command == "DISCONNECT":
                clients[clients[name]["connected_with"]]["client"].send(f"{name} has disconnected".encode())
                clients[name]["connected_with"] = ""
                clients[clients[name]["connected_with"]]["connected_with"] = ""

            elif command == "FILE":
                clients[clients[name]["connected_with"]]["file_name"] = data

            elif command == "SENDFILE":
                file_name = clients[name]["file_name"]
                file_size = clients[name]["file_size"]
                file_path = os.path.join("shared_files", file_name)

                with open(file_path, "wb") as file:
                    while file_size > 0:
                        if file_size >= BUFFER_SIZE:
                            data = client.recv(BUFFER_SIZE)
                        else:
                            data = client.recv(file_size)
                        file.write(data)
                        file_size -= BUFFER_SIZE

                clients[clients[name]["connected_with"]]["client"].send(f"{name}|{file_name}".encode())

            elif command == "RECEIVEFILE":
                file_name = data
                file_path = os.path.join("shared_files", file_name)
                file_size = os.path.getsize(file_path)

                clients[name]["client"].send(f"FILE|{file_name}|{file_size}".encode())

                with open(file_path, "rb") as file:
                    while file_size > 0:
                        if file_size >= BUFFER_SIZE:
                            data = file.read(BUFFER_SIZE)
                        else:
                            data = file.read(file_size)
                        clients[name]["client"].send(data)
                        file_size -= BUFFER_SIZE

        except Exception as e:
            print(e)
            break

# Function to accept connections from the client
def acceptConnections():
    # Getting the global variables along with its values
    global SERVER
    global clients

    # Running an infinite loop to accept incoming connections
    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            "client": client,
            "address": addr,
            "connected_with": "",
            "file_name": "",
            "file_size": 4096
        }

        print(f"Connection established with {client_name} : {addr}")
        thread = Thread(target=handleClient, args=(client, client_name,))
        thread.start()

# Function to create and run an FTP server
def FTP():
    global IP_ADDRESS

    # Creating an authorizer object
    authorizer = DummyAuthorizer()
    authorizer.add_user("lftpd", "lftpd", "shared_files", perm="elradfmw")

    # Creating an FTP handler object
    handler = FTPHandler
    handler.authorizer = authorizer

    # Creating an FTP server object
    server = FTPServer((IP_ADDRESS, 21), handler)
    server.serve_forever()

# Setup function to initialize the server
def setup():
    # Printing the heading "IP MESSENGER" at the centre with the help of formatting
    print('\033[95m' + "{:^80}".format("IP MESSENGER") + '\033[0m')

    # Getting the global variables along with its values
    global SERVER
    global IP_ADDRESS
    global PORT

    # Creating a socket for the server
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding the server to the IP address and the port number
    SERVER.bind((IP_ADDRESS, PORT))

    # Listening for maximum 100 incoming connections
    SERVER.listen(100)

    # Printing the waiting message at the centre with the help of formatting
    print('\033[93m' + "{:^80}".format("Waiting for incoming connections...") + '\033[0m')

    # Calling the accept connections function
    acceptConnections()

# Create and start a thread on the server side
setup_thread = Thread(target=setup)
setup_thread.start()

# Create and start a thread on the FTP server side
ftp_thread = Thread(target=FTP)
ftp_thread.start()