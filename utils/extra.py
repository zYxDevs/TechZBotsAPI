import wget
from telegraph import upload_file as uf

async def download(url):
    try:
        return wget.download(url)
    except Exception as e:
        return f"error {str(e)}"

async def telegraph(image,text):
    try:
        return f"https://telegra.ph/{uf(image)[0]}"
    except Exception as e:
        return f"https://techzbotsapi.herokuapp.com/logo?text={text}"

async def telegraph_simple(image):
    try:
        return f"https://telegra.ph/{uf(image)[0]}"
    except Exception as e:
        return str(e)