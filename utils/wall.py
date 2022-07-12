import asyncio
import random
import aiohttp 
from bs4 import BeautifulSoup as bs

async def search_wall(query):
    try:
        url = "https://wall.alphacoders.com/search.php?search=" + query.replace(' ','+')
        
        async with aiohttp.ClientSession() as session:
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
        return "error " + str(e)


async def search_wallpro(query):
    try:
        url = "https://wall.alphacoders.com/search.php?search=" + query.replace(' ','+')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                soup =bs(await resp.text(),"html.parser")
                images = soup.find_all("picture")

        wall_list = []

        for i in images:
            thumb = i.find_all("source")
            
            preview = str(thumb[1].get("srcset"))
            sd = str(thumb[2].get("srcset"))
            hd = str(i.find("img").get("src"))

            x = {}
            x["preview"] = preview
            x["sd"] = sd
            x["hd"] = hd

            wall_list.append(x)
        
        random.shuffle(wall_list)
        return wall_list
    except Exception as e:
        return "error " + str(e)