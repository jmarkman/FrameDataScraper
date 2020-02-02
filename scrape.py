# import FrameDataParser
import requests
from bs4 import BeautifulSoup

dkDataPage = requests.get("https://ultimateframedata.com/wario.php")

parsedDonkeyKongPage = BeautifulSoup(dkDataPage.text, 'lxml')

normals = parsedDonkeyKongPage.find_all("div", class_="moves")

jab = normals[0].find_all("div", class_="movecontainer")

print(jab[0].find("div", class_="movename").text)