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
import sys
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions

from selenium.webdriver.chrome.options import Options

# Using a mobile browser to open the categories webpage to then read out the links for each app
# Mobile browser is required cause the a normal browser loads content on scrolling and the mobile browser
# loads content when clicking the "show more button". The while loop eventually clicks that button... if it doesn't
# exist anymore then selenium raises an exception
chrome_options = Options()
chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('C:\\Users\\Tim\\Documents\\University\\Facher\\WIA\\src\\y.html')

'''
# show_more_btn = driver.find_element_by_id("show-more-button")
#show_more_btn = driver.find_element(By.CLASS_NAME, "XjE2Pb")
try:
    while True:
        driver.implicitly_wait(10)
        show_more_btn.click()
except selenium.common.exceptions.ElementNotVisibleException:
    pass
'''
# get all important links from the category page
category_page_source_code = driver.page_source.encode("utf-8")
soup = BeautifulSoup(category_page_source_code, "html.parser")
mydivs = soup.findAll("div", {"class": "wXUyZd"})
link_List = []
google_url = 'https://play.google.com'
for div in mydivs[1:]:
    m = re.search('class=\"card-click-target\" href=\"(.*)', str(div))

    anchors = div.findAll("a")

    link = str(anchors[0])
    link = link.replace("<a aria-hidden=\"true\" class=\"poRVub\" href=\"", "").replace("\" tabindex=\"-1\"></a>", "")
    print(link)
    # s1 = m.group(1)
    # link = s1.split("\">")[0]
    #  print(link)
    link_List.append(link)

print(len(link_List), "links")

final_Dic = {}
##link_List = ["https://play.google.com/store/apps/details?id=com.SongGameDev.EleTD", "https://play.google.com/store/apps/details?id=com.melesta.toydefense3"]

for game_url in link_List:

    print("URL", game_url)
    content = urlopen(game_url).read()
    soup = BeautifulSoup(content, "html.parser")

    title = soup.findAll("h1", {"class": "AHFaub"})[0].findAll("span")
    title = str(title[0].getText())
    print("Title", title)  # WORKS!

    try:
        rating = soup.findAll("div", {"class": "BHMmbe"})[0]
        rating = rating.getText()
        print("Rating", rating)  # WORKS!
    except:
        rating = "none"
        print("Rating", "none")  # WORKS!

    price = soup.findAll("span", {"class": "oocvOe"})[0].findAll("button")
    if price == "Install":
        price = str(price[0].getText())
    else:
        price = str(price[0].getText()).replace("€", "").replace(" Buy", "")

    print("Price", price)  # saying price or the string "Install" # WORKS!

    try:
        # print(soup.get_text())
        data = str(soup.get_text())
    except:
        pass  # everything else will mostly fail

    try:
        size = re.findall("Size*\d+MInstalls", data)[0].replace("Size", "").replace("Installs", "")  # WORKS!
        print("Size", size)
    except:
        size = 'err'

    try:
        installs = re.search(r'Installs(.*?)\+Current', data).group(1)
        print("No. Installations", installs)  # WORKS!
    except:
        installs = 'err'

    try:
        no_of_ratings_raw = re.search(r'stars by (.*?) people', data).group(1)
        print("No. Ratings", no_of_ratings_raw)
    except:
        no_of_ratings_raw = 'err'

    try:
        updated = re.search(r'Updated(.*?)Size', data).group(1)
        print("Updated", updated)
    except:
        updated = 'err'

    try:
        android_version = re.search(r'Requires Android(.*?) and up', data).group(1)
        print("Android", android_version)
    except:
        android_version = 'err'

    try:
        interactive_elements = re.search(r'Interactive Elements(.*?)PermissionsView', data).group(1)
        print("interactive_elements", interactive_elements)
    except:
        interactive_elements = 'err'

    try:
        devs = soup.findAll("div", {"class": "BgcNfc"})
        developer = "err"
        for dev in devs:
            if dev.getText() == "Developer":
                main_tag = dev.parent.get_text
                developer = re.search(r'href=(.*?)>Visit website', str(main_tag)).group(1)
                developer = str(developer[1:len(developer)-1])
                print("Developer", developer)
    except:
        developer = "err"

    final_Dic[title] = (game_url, price, rating, size, installs, no_of_ratings_raw, updated, android_version, interactive_elements, developer)

print(final_Dic)
columns = ["game_url", "price", "rating", "size", "installs", "no_of_ratings_raw", "updated", "android_version", "interactive_elements", "developer"]
df = pd.DataFrame.from_dict(final_Dic, orient='index', columns=columns)
df.to_csv("googlePlayStoreInsights.csv")