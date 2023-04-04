import socket
import threading
import os
import time


class Client():
    def __init__(self, HOST, PORT) -> None:
        self.host = HOST
        self.port = PORT
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))
        self.isNameSent = False
        self.recv()

    def recv(self):
        while True:
            try:
                cmd = self.client.recv(1024).decode("utf-8")
                if cmd == "YN" and self.isNameSent == False:
                    name = socket.gethostname()
                    self.client.send(name.encode("utf-8"))
                    self.isNameSent == True
                elif cmd == "-sI":
                    pass
                elif cmd == "-sC":
                    while True:
                        order = self.client.recv(1024).decode("utf-8")
                        if order == "brk":
                            break

                        elif order == "cd":
                            try:
                                dir = self.client.recv(1024).decode("utf-8")
                                if os.path.isdir(dir):
                                    os.chdir(dir)
                                    self.client.send(
                                        f"I'm in {os.getcwd()} right now.".encode("utf-8"))
                                else:
                                    self.client.send(
                                        f"There is no file in this name: {dir}.".encode("utf-8"))
                            except Exception as er:
                                self.client.send(f"{er}")

                        elif order == "tData":
                            print("I'm in tData")
                            try:
                                path = self.client.recv(1024).decode("utf-8")
                                file_size = os.path.getsize(path)
                                # self.client.send(f"fs@{str(file_size)}".encode("utf-8"))
                                pathSplit = path.split("/")
                                print(f"Path Split: {pathSplit}")
                                fileName = pathSplit[-1]
                                pathSplit.pop(-1)
                                nPath = ""
                                for i in pathSplit:
                                    nPath += f"{i}/"
                                print(f"Path: {nPath}")
                                print(f"File Name: {fileName}")
                                print(f"File Size: {str(file_size)}")
                                with open(path, "rb") as file:
                                    c = 0
                                    print("Sending started")
                                    while c <= file_size:
                                        data = file.read(1024)
                                        if not (data):
                                            break
                                        self.client.sendall(data)
                                        c += len(data)

                            except Exception as er:
                                self.client.send(
                                    f"I could'nt find the file {er}".encode("utf-8"))

                        elif order == "dir":
                            try:
                                for i in range(len(os.listdir())):
                                    self.client.send(
                                        f"--:: {i+1}. {os.listdir()[i]}".encode("utf-8"))
                            except Exception as er:
                                self.client.send(
                                    f"An Error Occurred: {er}".encode("utf-8"))
                        elif order == "cwd":
                            self.client.send(os.getcwd().encode("utf-8"))

                        elif order == "mkd":
                            try:
                                dir = self.client.recv(1024).decode("utf-8")
                                os.mkdir(dir)
                                self.client.send(
                                    f"{dir} has been created.".encode("utf-8"))
                            except Exception as er:
                                self.client.send(
                                    f"There is a file in same name: {er}".encode("utf-8"))

                        elif order == "rmd":
                            try:
                                dir = self.client.recv(1024).decode("utf-8")
                                os.rmdir(dir)
                                self.client.send(
                                    f"{dir} has been removed.".encode("utf-8"))
                            except Exception as er:
                                self.client.send(
                                    f"There is no file in this name: {er}".encode("utf-8"))

                        elif order == "rnd":
                            try:
                                dir = self.client.recv(1024).decode("utf-8")
                                newName = self.client.recv(
                                    1024).decode("utf-8")
                                os.rename(dir, newName)
                                self.client.send(
                                    f"{dir} has been changed to {newName}.".encode("utf-8"))
                            except Exception as er:
                                self.client.send(
                                    f"There is no file in this name or there is a file in new name: {er}".encode("utf-8"))

                elif cmd == "-dc":
                    self.client.close()
                    break

                elif cmd == "-sM":
                    print("I'm in -sM")
                    msg = self.client.recv(1024).decode("utf-8")
                    print(msg)

            except Exception as er:
                print("An error occurred: ", er)
                self.client.close()
                break


client = Client(socket.gethostname(), 59999)

# path = self.client.recv(1024).decode("utf-8")
# with open(f"{path}", "rb") as f:
#     file = f.read()
# self.client.send(f"f@{file}".encode("utf-8"))
