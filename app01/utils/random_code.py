import random
import string
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

str_all = string.digits + string.ascii_letters + string.digits


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def random_code(size=(200, 40), length=4, point_num=1000, line_num=10):
    width, height = size
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font='static/my/font/code.ttf', size=32)
    valid_code = ""
    for i in range(length):
        random_char = random.choice(str_all)
        draw.text((40 * i + 20, 0), random_char, (0, 0, 0), font=font)
        valid_code += random_char
    # 随机画点
    for i in range(point_num):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), random_color())
    # 随机划线
    for i in range(line_num):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, height), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())
    # 创建一个内存句柄
    f = BytesIO()
    # 将图片保存到内存句柄中
    img.save(f, 'PNG')
    data = f.getvalue()
    return (data,valid_code)


if __name__ == '__main__':
    random_code()
