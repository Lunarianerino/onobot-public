from PIL import ImageFont

username_font = ImageFont.truetype(font='./cogs/fonts/Kuro-Regular.otf', size = 20)
print(username_font)
print(username_font.size)

username_font.size = 10
print(username_font)
print(username_font.size)