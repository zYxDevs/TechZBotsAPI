import requests
from bs4 import BeautifulSoup as bs

async def get_unsplash(query):
    try:
        link = "https://unsplash.com/s/photos/" + query.replace(" ","-")    
        res = requests.get(link)
        soup = bs(res.content, "html.parser")
        div = soup.find_all("div", class_="mef9R")

        images = []

        for i in div:
            a = i.find('a').get("href")
            images.append(a)

        return images
    except Exception as e:
        return str(e)

dict = "a"

print(str(type(dict)))