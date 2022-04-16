import aiohttp
from telegraph import upload_file as uf

async def download(url):
    try:
        x = url.split('/')
        file = x[-1]

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                open(file,"wb").write(resp.content)

        return file
    except Exception as e:
        return "error " + str(e)

async def telegraph(image):
    try:
        url = "https://telegra.ph/" + uf(image)
        return url
    except Exception as e:
        return "error " + str(e)