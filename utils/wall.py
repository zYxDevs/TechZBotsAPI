import random
import aiohttp 
from bs4 import BeautifulSoup as bs

session = aiohttp.ClientSession()

async def search_wall(query):
    try:
        url = "https://wall.alphacoders.com/search.php?search=" + query.replace(' ','+')
        
        async with session:
            async with session.get(url) as resp:
                soup =bs(await resp.text(),"html.parser")
                images = soup.find_all("img","big-thumb")

        final_list = []

        for i in images:
            url = i.get("src")
            x = url.split("/")
            id = x[3]
            image_id = x[4].replace("thumbbig-","")
            domain = x[2]

            # same pattern in all alphacoder wallpapers
            imgurl = f"https://{domain}/{id}/{image_id}" # high quality image
            final_list.append(imgurl)

        # shuffling list
        random.shuffle(final_list)
        return final_list
    except Exception as e:
        return str(e)