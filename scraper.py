# a small web scraper to scrape data

import re
from bs4 import *  # stands for Beautiful Soup version 4
from urllib.request import Request, urlopen
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


market_url = 'x.html'
google_url = 'https://play.google.com'

# get all important links
soup = BeautifulSoup(open("x.html"))
mydivs = soup.findAll("div", {"class": "card no-rationale square-cover apps small"})

link_List =  []
for div in mydivs:
    m = re.search('class=\"card-click-target\" href=\"(.*)', str(div))
    s1 = m.group(1)
    link = s1.split("\">")[0]
    #  print(link)
    link_List.append(google_url+link)

print(len(link_List))

game_url = link_List[0]
final_Dic = {}

for game_url in link_List:

    driver = webdriver.Chrome("C:\webdrivers\chromedriver.exe")


    driver.get(game_url)
    try:
        elem = driver.find_element_by_class_name('AHFaub')
        title = elem.text
    except:
        title = "err"

    try:
        elem = driver.find_element_by_class_name('BHMmbe')
        rating = elem.text
    except:
        rating = "err"

    try:
        elem = driver.find_element_by_class_name('oocvOe')
        price =elem.text
    except:
        price = 'err'

    try:
        elem = driver.find_element_by_class_name('xyOfqd')
        data = str(elem.text).splitlines()
        try:
            size = data[data.index("Size")+1]
        except:
            size = 'err'
        try:
            installationen = data[data.index("Installs")+1]
        except:
            installationen = 'err'
    except:
        size = 'err'
        installationen = 'err'

    print(title, size, installationen, price, rating)

    final_Dic[title] = (installationen, price, rating, size)
    df = pd.DataFrame.from_dict(final_Dic)
    df.to_csv("googlePlayStoreInsights.csv")

    driver.close()

print(final_Dic)

