import os
from fastapi import FastAPI
from utils import search_unsplash, search_wall, telegraph, generate_logo
from fastapi.responses import RedirectResponse, FileResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"status": "TechZBots - Api working fine..."}


@app.get("/wall")
async def read_item(query: str):
    data = await search_wall(query)

    if str(type(data)) == "<class 'str'>":
        return {"success": "False", "error": f"{data}"}

    return {"success": "True", "images": data}

@app.get("/unsplash")
async def read_item(query: str):
    data = await search_unsplash(query)

    if str(type(data)) == "<class 'str'>":
        return {"success": "False", "error": f"{data}"}

    return {"success": "True", "images": data}

@app.get("/logo")
async def read_item(text: str):
    text = text.replace("%20"," ").upper().strip()
    data = await generate_logo(text)

    if "error" in str(data):
        error = data.replace("error",'').strip()
        return {"success": "False", "error": f"{error}"}

    file_size = int(os.path.getsize(data))

    if file_size < 4800000:
        telegraph_link = await telegraph(data)
        if "error" in str(data):
            error = data.replace("error",'').strip()
            return {"success": "False", "error": f"{error}"}
        return RedirectResponse(telegraph_link)

    return FileResponse(data)
