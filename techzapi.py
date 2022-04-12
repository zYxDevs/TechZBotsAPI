from fastapi import FastAPI

# modules

from modules.unsplash import get_unsplash

app = FastAPI()


@app.get("/")
async def read_root():
    return {"TechZBots": "Api working fine..."}


@app.get("/wall/{query}")
async def read_item(query):
    data = await get_unsplash(query)

    if str(type(data)) == "<class 'str'>":
        return {"success": "False", "error": f"{data}"}

    return {"success": "True", "images": data}
