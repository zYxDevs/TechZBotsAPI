import asyncio
import os
from typing import Optional
from fastapi import FastAPI
from utils import search_unsplash, search_wall, telegraph, generate_logo, get_nyaa_info
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
async def get_nyaa(code: int):
    "Get info from nyaa using code"
    x = await get_nyaa_info(code)
    return x