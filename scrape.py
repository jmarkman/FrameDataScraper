import requests
import webbrowser

from bs4 import BeautifulSoup

dkDataPage = requests.get("https://ultimateframedata.com/donkey_kong.php")

parsedDonkeyKongPage = BeautifulSoup(dkDataPage.text, 'lxml')

normals = parsedDonkeyKongPage.find_all("div", class_="moves")

print(normals[0])