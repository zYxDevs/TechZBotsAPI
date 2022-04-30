import wget
from telegraph import upload_file as uf

async def download(url):
    try:
        filename = wget.download(url)
        return filename
    except Exception as e:
        return "error " + str(e)

async def telegraph(image):
    try:
        url = "https://telegra.ph/" + uf(image)[0]
        return url
    except Exception as e:
        return "error " + str(e)
