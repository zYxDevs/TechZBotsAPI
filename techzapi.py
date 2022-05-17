import asyncio
import os
from typing import Optional
from utils import thumbnail
from utils.thumbnail import gen_thumb
from fastapi import FastAPI
from utils import *
from fastapi.responses import RedirectResponse, FileResponse

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "TechZBots - Api working fine..."}


@app.get("/wall")
async def get_wall(query: str):
    "Get direct links of wallpapers"
    data = await search_wall(query)

    if str(type(data)) == "<class 'str'>":
        return {"success": "False", "error": f"{data}"}

    return {"success": "True", "images": data}

@app.get("/unsplash")
async def get_unsplash(query: str):
    "Get direct links of images from unsplash"
    data = await search_unsplash(query)

    if str(type(data)) == "<class 'str'>":
        return {"success": "False", "error": f"{data}"}

    return {"success": "True", "images": data}

@app.get("/logo")
async def make_logo(text: str, square: Optional[bool] = None):
    "Generate a random logo"
    text = text.replace("%20"," ").replace("+"," ").replace("_"," ").upper().strip()
    
    data = await generate_logo(text,str(square))

    if "error" in str(data):
        error = data.replace("error",'').strip()
        return {"success": "False", "error": f"{error}"}

    file_size = int(os.path.getsize(data))

    if file_size < 4800000:
        telegraph_link = await telegraph(data,text)
        if "error" in str(data):
            error = data.replace("error",'').strip()
            return {"success": "False", "error": f"{error}"}
        return RedirectResponse(telegraph_link)

    return FileResponse(data)


@app.get("/nyaa")
async def get_nyaa(code):
    "Get info from nyaa using code"
    x = await get_nyaa_info(code=code)
    return x



@app.get("/ud")
async def get_ud(word: str, max: Optional[int] = None):
    "Get meaning of a word from urban dictionary"
    x = await get_urbandict(word)
    z = {}
    if len(x) > 0:
      z['success'] = 'True'
    else:
      z['success'] = 'False'
      z['error'] = 'Word Not Found'
      
    z['word'] = word
    if max:
      x = x[:max]
    z['results'] = x
    return z

@app.get("/torrent")
async def torrent(query: str, max: Optional[int] = None):
  "Get Torrent currently only yts supported"
  x = await yts(query)
  res = {}
  if x:
    res['success'] = 'True'
    res['query'] = query
    res['results'] = x
  else:
    res['success'] = 'False'
    res['error'] = 'Results Not Found'

  return res

@app.get("/lyrics")
async def search_lyrics(query: str):
    "Search lyrics"
    lyrics = await get_lyrics(query)

    data = {}

    data["success"] = 'True'
    data["query"] = query
    data["lyrics"] = lyrics
    return data

@app.get("/thumb")
async def generate_thumbnail(videoid: str, botname: Optional[str] = None):
    "Generate thumbnail"

    if not botname:
      botname = "SiestaXMusic"
    thumb = await gen_thumb(videoid,botname)

    return RedirectResponse(thumb)
