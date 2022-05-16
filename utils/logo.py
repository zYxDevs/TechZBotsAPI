from utils import search_unsplash, download
import random, glob, asyncio
from PIL import Image, ImageDraw, ImageFont, ImageOps
from typing import Optional

# colors = [(255, 170, 51), (220, 20, 60), (255, 215, 0), (52, 52, 52), (48, 25, 52), (191, 64, 191), (31, 81, 255), (255, 191, 0), (210, 4, 45), (224, 17, 95), (53, 57, 53), (54, 69, 79), (0, 150, 255), (128, 0, 128), (0, 255, 255), (0, 0, 0), (218, 112, 214), (93, 63, 211), (255, 0, 255), (127, 0, 255), (2, 48, 32), (25, 25, 112), (50, 205, 50), (255, 165, 0), (124, 252, 0), (40, 40, 43), (80, 200, 120), (255, 234, 0), (255, 105, 180), (255, 68, 51), (255, 127, 80), (93, 63, 211), (50, 205, 50), (124, 252, 0), (255, 36, 0), (238, 75, 43), (215, 0, 64), (255, 172, 28), (27, 18, 18), (255, 0, 0)]
search = ["blur background", "background", "neon lights", "wallpaper", "asthetic", "anime", "abstract", "dark", "shape", "pattern", "gradient", "colorful", "nature"]
 
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

def make_col():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def get_colours():
    font_color = make_col()
    stroke_color = make_col()
    border_color = make_col()
    border_color2 = make_col()

    return font_color, stroke_color, border_color, border_color2

def get_sizes(text, font, img, width_ratio):
    # font size
    font_size = find_font_size(text, font, img, width_ratio)

    # border
    width, height = img.size
    if width > height:    
        brdor = round((2/100) * height)
    else:
        brdor = round((2/100) * width)

    # font size modify
    if font_size > width or font_size > height:
        if width > height:
            font_size = round(width/2)
        else:
            font_size = round(height/2)

    # stroke width 
    if font_size < 300:
        stroke_width = round((5/100) * font_size)
    else:
        stroke_width = round((10/100) * font_size)

    return font_size, brdor, width, height, stroke_width

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

async def generate_logo(text: str, square: Optional[str] = None):
    image_file = await get_image()
    
    fpath = glob.glob("resources/fonts/*")
    font = random.choice(fpath)
    
    width_ratio = 0.7    
    img = Image.open(image_file)  

    # if square = true then croping image as a square
    if str(square).capitalize() == "True":
        x = min(img.size)
        w, h = img.size
        img = img.crop(((w - x) // 2,(h - x) // 2,(w + x) // 2,(h + x) // 2))

    draw = ImageDraw.Draw(img)
    font_color, stroke_color, border_color, border_color2 = get_colours()
    font_size, brdor, width, height, stroke_width = get_sizes(text, font, img, width_ratio)

    font = ImageFont.truetype(font, font_size)
    w, h = draw.textsize(text, font=font)
    draw.text(
        ((width - w) / 2, (height - h) / 2),
        text,
        font=font,
        fill=font_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color,
    )
    
    # making border
    img = ImageOps.expand(img,border=brdor,fill=border_color)
    img = ImageOps.expand(img,border=brdor,fill=border_color2)

    file_name = "temp_files/" + str(random.randint(11111111,99999999)) + ".jpg"
    img.save(file_name)
    return file_name
