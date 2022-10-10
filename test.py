from PIL import Image, ImageDraw, ImageFont

img = Image.new("RGB", (100, 30), color=(73, 109, 137))

fnt = ImageFont.truetype("C:\Windows\Fonts/Arial.ttf", 15)
d = ImageDraw.Draw(img)
d.text((10, 10), "Hello world", font=fnt, fill=(255, 255, 0))

img.save("a.png")
