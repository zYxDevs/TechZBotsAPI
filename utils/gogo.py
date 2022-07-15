import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
}
cookies = {
    #  'cf_clearance': 'a8e8039fcefafd6a515195186980c54399b80c4f-1626262802-0-250',
    #  'prefetchAd_4732994': 'true',
    #  'prefetchAd_3386133': 'true',
}

from selenium import webdriver
import sys
import re
import os
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
firefox_options.add_argument("--private-window")

def getDownloadPageHTML(url):
    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    browser = webdriver.Firefox(firefox_binary=binary,executable_path=os.environ.get('GECKODRIVER_PATH'),options=firefox_options)
        
    try:
        timeout = 15
        browser.get(url)
        what_is_this = WebDriverWait(browser, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, "//body/section" + "/div" * 6 + "/a")
            )
        )

        x = BeautifulSoup(browser.page_source, "html.parser")
        browser.quit()
        return 0,x
    except TimeoutException as x:
        return 1,x


def get_gogo(url):
    x,soup = getDownloadPageHTML(url)

    if x == 1:
        return soup
    episodes = []

    links = soup.find_all('div', class_='dowload')

    for i in links:
        link = i.find('a').get('href')
        res = i.text.replace('Download','').replace('\n','').strip()

        if 'Ad' not in res:
            episodes.append((res,link))

    return episodes

def get_vid(url):
    r = requests.get(url,headers=headers,cookies=cookies)
    soup = bs(r.content, "html.parser")
    source_url = soup.find("li", {"class": "dowloads"}).a
    link = source_url.get('href')
    return link


def gogo_scrapper(url):
    x = get_vid(url)
    x = get_gogo(x)

    return x