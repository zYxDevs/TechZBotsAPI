import os, json
from fastapi import FastAPI
from utils import search_unsplash, search_wall, telegraph, generate_logo, get_nyaa_info
from fastapi.responses import RedirectResponse, FileResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"status": "TechZBots - Api working fine..."}


@app.get("/wall")
async def read_item(query: str):
    "Get direct links of wallpapers"
    data = await search_wall(query)

    if str(type(data)) == "<class 'str'>":
        return {"success": "False", "error": f"{data}"}

    return json.dumps({"success": "True", "images": data}, indent=4)

@app.get("/unsplash")
async def read_item(query: str):
    "Get direct links of images from unsplash"
    data = await search_unsplash(query)

    if str(type(data)) == "<class 'str'>":
        return json.dumps({"success": "False", "error": f"{data}"}, indent=4)

    return json.dumps({"success": "True", "images": data}, indent=4)

@app.get("/logo")
async def read_item(text: str):
    "Generate a random logo"
    text = text.replace("%20"," ").upper().strip()
    data = await generate_logo(text)

    if "error" in str(data):
        error = data.replace("error",'').strip()
        return json.dumps({"success": "False", "error": f"{error}"}, indent=4)

    file_size = int(os.path.getsize(data))

    if file_size < 4800000:
        telegraph_link = await telegraph(data,text)
        if "error" in str(data):
            error = data.replace("error",'').strip()
            return json.dumps({"success": "False", "error": f"{error}"}, indent=4)
        return RedirectResponse(telegraph_link)

    return FileResponse(data)


@app.get("/nyaa")
async def get_nyaa(code: int):
  "Get info from nyaa using code"
  x = await get_nyaa_info(code)
  return json.dumps(x, indent=4)
