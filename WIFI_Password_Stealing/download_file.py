import requests

def download(url):
	get_response = requests.get(url)
	filename = url.split("/")[-1]
	with open(filename, "wb") as out_file:
		out_file.write(get_response.content)

download("https://www.hdwallpaper.nu/wp-content/uploads/2017/08/ponyo-4.jpg")
