from utils import search_unsplash, download
import random, glob
from PIL import Image, ImageDraw, ImageFont, ImageOps

colors = [(255, 170, 51), (220, 20, 60), (255, 215, 0), (52, 52, 52), (48, 25, 52), (191, 64, 191), (31, 81, 255), (255, 191, 0), (210, 4, 45), (224, 17, 95), (53, 57, 53), (54, 69, 79), (0, 150, 255), (128, 0, 128), (0, 255, 255), (0, 0, 0), (218, 112, 214), (93, 63, 211), (255, 0, 255), (127, 0, 255), (2, 48, 32), (25, 25, 112), (50, 205, 50), (255, 165, 0), (124, 252, 0), (40, 40, 43), (80, 200, 120), (255, 234, 0), (255, 105, 180), (255, 68, 51), (255, 127, 80), (93, 63, 211), (50, 205, 50), (124, 252, 0), (255, 36, 0), (238, 75, 43), (215, 0, 64), (255, 172, 28), (27, 18, 18), (255, 0, 0)]
search = ["blur background", "background", "neon lights", "wallpaper", "asthetic", "anime", "abstract", "dark"]
 
async def get_image():
    try:
        # getting image from unsplash    
        word = random.choice(search)

        image_url = await search_unsplash(word)
        image_url = random.choice(image_url)
        image_file = await download(image_url)

        return image_file
    except Exception as e:
        return "error " + str(e)

def get_text_size(text, image, font):
    im = Image.new("RGB", (image.width, image.height))
    draw = ImageDraw.Draw(im)
    return draw.textsize(text, font)

def find_font_size(text, font, image, target_width_ratio):
    tested_font_size = 100
    tested_font = ImageFont.truetype(font, tested_font_size)
    observed_width, observed_height = get_text_size(
        text, image, tested_font
    )
    estimated_font_size = (
        tested_font_size / (observed_width / image.width) * target_width_ratio
    )
    return round(estimated_font_size)

async def generate_logo(text):
    try:
        image_file = await get_image()
        
        fpath = glob.glob("resources/fonts/*")
        font = random.choice(fpath)

        if len(text) <= 8:
            strke = 8
        elif len(text) >= 9:
            strke = 3

        fill = random.choice(colors)
        width_ratio = 0.7
        stroke_width = strke
        stroke_fill = random.choice(colors)

        img = Image.open(image_file)
        width, height = img.size
        draw = ImageDraw.Draw(img)
        font_size = find_font_size(text, font, img, width_ratio)
        font = ImageFont.truetype(font, font_size)
        w, h = draw.textsize(text, font=font)
        draw.text(
            ((width - w) / 2, (height - h) / 2),
            text,
            font=font,
            fill=fill,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        
        # making border
        img = ImageOps.expand(img,border=10,fill=random.choice(colors))

        file_name = str(random.randint(111111,999999)) + ".png"
        img.save(f"./temp_files/{file_name}", "PNG")
        return file_name
    except Exception as e:
        return "error " + str(e)