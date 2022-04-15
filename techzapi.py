from fastapi import FastAPI
from utils import search_unsplash, search_wall
import aiohttp

app = FastAPI()

session = aiohttp.ClientSession()

@app.get("/")
async def read_root():
    return {"status": "TechZBots - Api working fine..."}


@app.get("/wall/{query}")
async def read_item(query):
    data = await search_wall(query)

    if str(type(data)) == "<class 'str'>":
        return {"success": "False", "error": f"{data}"}

    return {"success": "True", "images": data}

@app.get("/unsplash/{query}")
async def read_item(query):
    data = await search_unsplash(query)

    if str(type(data)) == "<class 'str'>":
        return {"success": "False", "error": f"{data}"}

    return {"success": "True", "images": data}