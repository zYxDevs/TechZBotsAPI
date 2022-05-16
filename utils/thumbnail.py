import asyncio
import os
import re
from utils import telegraph_simple

import aiofiles
import aiohttp
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter,
                 ImageFont, ImageOps)
from youtubesearchpython.__future__ import VideosSearch
import numpy as np

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def truncate(text):
    list = text.split(" ")
    text1 = ""
    text2 = ""    
    for i in list:
        if len(text1) + len(i) < 24:        
            text1 += " " + i
        elif len(text2) + len(i) < 24:        
            text2 += " " + i

    text1 = text1.strip()
    text2 = text2.strip()     
    return [text1,text2]

async def gen_thumb(videoid,bot_name):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(
                        f"cache/thumb{videoid}.png", mode="wb"
                    )
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(30))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.6)
        Xcenter = youtube.width / 2
        Ycenter = youtube.height / 2
        x1 = Xcenter - 250
        y1 = Ycenter - 250
        x2 = Xcenter + 250
        y2 = Ycenter + 250
        logo = youtube.crop((x1, y1, x2, y2))
        logo.thumbnail((520, 520), Image.ANTIALIAS)
                                                                                        
        circle = Image.open("resources/images/circle.png")

        image3 = image1.crop((280,0,1000,720))
        lum_img = Image.new('L', [720,720] , 0)
        draw = ImageDraw.Draw(lum_img)
        draw.pieslice([(0,0), (720,720)], 0, 360, fill = 255, outline = "white")
        img_arr = np.array(image3)
        lum_img_arr = np.array(lum_img)
        final_img_arr = np.dstack((img_arr,lum_img_arr))
        image3 = Image.fromarray(final_img_arr)
        image3 = image3.resize((600,600))

        image2.paste(image3, (50,70), mask = image3)
        image2.paste(circle, (0,0), mask = circle)

        # fonts
        font1 = ImageFont.truetype(r'resources/images/arial_bold.ttf', 30)
        font2 = ImageFont.truetype(r'resources/images/arial_black.ttf', 60)
        font3 = ImageFont.truetype(r'resources/images/arial_black.ttf', 40)
        font4 = ImageFont.truetype(r'resources/images/arial_bold.ttf', 35)

        image4 = ImageDraw.Draw(image2)
        image4.text((10, 10), bot_name, fill="white", font = font1, align ="left") 
        image4.text((670, 150), "NOW PLAYING", fill="white", font = font2, align ="left") 

        # title
        title1 = truncate(title)
        image4.text((670, 300), text=title1[0], fill="white", font = font3, align ="left") 
        image4.text((670, 350), text=title1[1], fill="white", font = font3, align ="left") 

        # description
        views = f"Views : {views}"
        duration = f"Duration : {duration} Mins"
        channel = f"Channel : {channel}"

        image4.text((670, 450), text=views, fill="white", font = font4, align ="left") 
        image4.text((670, 500), text=duration, fill="white", font = font4, align ="left") 
        image4.text((670, 550), text=channel, fill="white", font = font4, align ="left")

        image2.save(f"cache/{videoid}.png")
        file = f"cache/{videoid}.png"
        telegraph_link = await telegraph_simple(file)

        return telegraph_link
    except Exception as e:
        print(e)
        return "https://telegra.ph/file/e17f42bc195635b668d6d.jpg"