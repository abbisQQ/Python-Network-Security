import requests
import re
import urllib.parse
from requests.exceptions import InvalidSchema


target_url = "https:/exampletarget.com"

target_list = []

#Gets all the links in this web page
def extract_links_from(url):
    try:
        response = requests.get(url)
        return re.findall('(?:href=")(.*?)"',str(response.content))
    except InvalidSchema:
            pass  # It's probably FTP :



def crawl(url):
    href_links = extract_links_from(url)

    for link in href_links:
        link = urllib.parse.urljoin(url, link)
        # removes # links keeping only the first part of this split, this help us get only unique paths
        if "#" in link:
            link = link.split('#')[0]

        # removes external links
        if url in link and link not in target_list:
            target_list.append(link)
            print(link)
            # crawl inside every link finding every internal link before moving to another one.
            crawl(link)


crawl(target_url)
