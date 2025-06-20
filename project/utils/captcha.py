import random, string
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.cache import cache

def generate_captcha_text(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def generate_captcha_image(text):
    width, height = 150, 50
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 32)  # Use a custom font if available
    except:
        font = ImageFont.load_default()

    draw.text((10, 5), text, font=font, fill=(0, 0, 0))

    for _ in range(50):  # Noise
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()
