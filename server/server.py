import socket
import threading
import time


class Server():
    def __init__(self, HOST, PORT) -> None:
        self.clients = []
        self.names = []
        self.host = HOST
        self.port = PORT
        self.filePath = ""
        self.clientIndex = 0
        self.file_size = 0
        self.file = ""
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        print("Server has been started.")
        self.server.listen()
        self.connect()

    def connect(self):
        while True:
            try:
                client, addr = self.server.accept()
                print(
                    f"""
                    New Client Connected
                    {client}
                    {addr}
                """)
                client.send("YN".encode("utf-8"))
                name = client.recv(1024).decode("utf-8")
                self.clients.append(client)
                self.names.append(name)
                sendCmdT = threading.Thread(target=self.sendCommand)
                recvT = threading.Thread(target=self.recv, args=(client,))
                recvT.start()
                if len(self.clients) == 1:
                    sendCmdT.start()
            except Exception as er:
                print("An error occurred on connection.")
                recvT.join()
                sendCmdT.join()
                break

    def sendCommand(self):
        while True:
            cmd = input("Command: ")
            if cmd == "-h":
                print("""
                    -sA Show all clients
                    -sC Send command to client's cmd | -sC-H for help
                    -sM Sends message to selected client
                    """)

            elif cmd == "-sN":  # Show names
                for i in range(0, len(self.names)):
                    print(f"{i+1}. {self.names[i]}")

            elif cmd == "-sC":  # Send command
                clientIndex = self.getIndex()
                self.clients[clientIndex].send(cmd.encode("utf-8"))
                while True:
                    try:
                        order = input("Order: ")
                        if order == "brk":
                            self.clients[clientIndex].send(
                                order.encode("utf-8"))
                            break

                        elif order == "tData":
                            self.clients[clientIndex].send(
                                order.encode("utf-8"))
                            self.clientIndex = clientIndex
                            path = input("Enter Path: ")
                            self.clients[clientIndex].send(
                                path.encode("utf-8"))
                            pathSplit = path.split("/")
                            self.fileName = pathSplit[-1]
                            pathSplit.pop(-1)
                            nPath = ""
                            for i in pathSplit:
                                nPath += f"{i}/"
                            self.filePath = f"{nPath}"

                            # path = input("Enter path: ")
                            # self.clients[clientIndex].send(
                            #     order.encode("utf-8"))
                            # self.clients[clientIndex].send(
                            #     path.encode("utf-8"))
                            # path = path.split("/")
                            # with open(f"database/{path[-1]}", "w") as f:
                            #     f.write(self.file)

                        elif order == "cd":  # Change dir
                            dir = input("Directory: ")
                            self.clients[clientIndex].send(
                                order.encode("utf-8"))
                            self.clients[clientIndex].send(
                                dir.encode("utf-8"))

                        elif order == "dir":  # List dir
                            self.clients[clientIndex].send(
                                order.encode("utf-8"))

                        elif order == "cwd":  # See current dir
                            self.clients[clientIndex].send(
                                order.encode("utf-8"))

                        elif order == "mkd":  # Create dir
                            dir = input("Directory Name: ")
                            self.clients[clientIndex].send(
                                order.encode("utf-8"))
                            self.clients[clientIndex].send(
                                dir.encode("utf-8"))

                        elif order == "rmd":  # Remove dir
                            dir = input("Directory Name: ")
                            self.clients[clientIndex].send(
                                order.encode("utf-8"))
                            self.clients[clientIndex].send(
                                dir.encode("utf-8"))

                        elif order == "rnd":  # Rename dir
                            dir = input("Directory Name: ")
                            newName = input("New Name : ")
                            self.clients[clientIndex].send(
                                order.encode("utf-8"))
                            self.clients[clientIndex].send(
                                dir.encode("utf-8"))
                            self.clients[clientIndex].send(
                                newName.encode("utf-8"))

                        elif order == "-sC-H":  # Help for -sC
                            print("""
                                    brk - Exit
                                    cd - Change directory
                                    dir - See content of a directory
                                    cwd - See current directory you are in
                                    mkd - Create directory
                                    rmd - Remove directory
                                    rnd - Rename directory
                                    """)

                    except Exception as er:
                        print("An error occurred in order: ", er)

            elif cmd == "-dc":  # Disconnect
                clientIndex = self.getIndex()
                self.clients[clientIndex].close()

                print(
                    f"Connection of {self.clients[clientIndex]} has been closed.")

            elif cmd == "-sM":  # Send message
                clientIndex = self.getIndex()
                self.clients[clientIndex].send(cmd.encode("utf-8"))
                self.clients[clientIndex].send(
                    input("Your Message: ").encode("utf-8"))
            else:
                print("Invalid Command")

    def recv(self, client):
        while True:
            try:
                msg = client.recv(1024).decode("utf-8")
                msg = msg.split("@")
                print(msg)
                if (msg[0] == "fs"):
                    while True:
                        print("I run")
                        try:
                            self.file_size = int(msg[1])
                            print(self.file_size)
                            with open("database/" + self.filePath.split("/")[-1], "wb") as file:
                                c = 0
                                # Starting the time capture.
                                start_time = time.time()

                                # Running the loop while file is recieved.
                                print("Receiving started")
                                while c <= int(self.file_size):
                                    data = self.clients[self.clientIndex].recv(
                                        1024)
                                    if not (data):
                                        break
                                    file.write(data)
                                    c += len(data)

                                # Ending the time capture.
                                end_time = time.time()

                            print(
                                f"File transfer Complete.Total time: {end_time - start_time}")
                            break
                        except Exception as er:
                            print(er)
                else:
                    print(msg[0])

            except Exception as er:
                print("AN ERROR OCCURRED ON CLIENT'S CONNTECTION ")
                clientIndex = self.clients.index(client)
                print(f"{self.names[clientIndex]} is offline.")
                self.names.pop(clientIndex)
                self.clients.remove(client)
                client.close()

    def getIndex(self):
        while True:
            try:
                clientIndex = int(
                    input("Which client you selected(Number): "))
                if clientIndex == 0 or clientIndex > len(self.clients):
                    print(
                        f"Number must be true. 0 - {len(self.clients)} includes and among numbers can be used.")
                else:
                    return clientIndex - 1
            except:
                print("Enter Integer Value")


server = Server(socket.gethostname(), 59999)
