# coding: utf-8;
###############################################################################
#
# AUTHOR: Tim Schäfer
# PYTHON: 3.7
# DESCRIPTION:
#
###############################################################################

import re
from bs4 import *  # stands for Beautiful Soup version 4
from urllib.request import Request, urlopen
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions

from selenium.webdriver.chrome.options import Options
'''
# Using a mobile browser to open the categories webpage to then read out the links for each app
# Mobile browser is required cause the a normal browser loads content on scrolling and the mobile browser
# loads content when clicking the "show more button". The while loop eventually clicks that button... if it doesn't
# exist anymore then selenium raises an exception
chrome_options = Options()
chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://play.google.com/store/search?q=tower+defense&c=apps')

show_more_btn = driver.find_element_by_id("show-more-button")
try:
    while True:
        driver.implicitly_wait(10)
        show_more_btn.click()
except selenium.common.exceptions.ElementNotVisibleException:
    pass

# get all important links from the category page
category_page_source_code = driver.page_source.encode("utf-8")
soup = BeautifulSoup(category_page_source_code, "html.parser")
mydivs = soup.findAll("div", {"class": "card no-rationale square-cover apps small"})
link_List =  []
google_url = 'https://play.google.com'
for div in mydivs:
    m = re.search('class=\"card-click-target\" href=\"(.*)', str(div))
    s1 = m.group(1)
    link = s1.split("\">")[0]
    #  print(link)
    link_List.append(google_url+link)

print(len(link_List))
'''
final_Dic = {}
link_List = ["https://play.google.com/store/apps/details?id=com.SongGameDev.EleTD", "https://play.google.com/store/apps/details?id=com.melesta.toydefense3"]

for game_url in link_List:
    print(game_url)
    content = urlopen(game_url).read()
    soup = BeautifulSoup(content, "html.parser")

    title = soup.findAll("h1", {"class": "AHFaub"})[0].findAll("span")
    print(title[0].getText())

    rating = soup.findAll("div", {"class": "BHMmbe"})[0]
    print(rating.getText())

    price = soup.findAll("span", {"class": "oocvOe"})[0].findAll("button")
    print(price[0].getText())

    try:
        elem = soup.findAll("div", {"class": "xyOfqd"})[0]
        #elem = driver.find_element_by_class_name('xyOfqd')
        data = str(elem.getText())

        x = re.findall("Size*\d+", data)
        print(x[0])

        try:
            print(data[data.index("Size"):data.index("Size")+5])
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

    print(size, installationen)
'''
for game_url in link_List:

    # TODO why do we need selenium here???
    # Maybe both options may be cool and seleneium only for a big overciew and bs4 for a quick one
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
'''
