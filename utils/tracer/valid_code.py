import random

def get_random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def get_validCode_img(request):

    from PIL import Image,ImageDraw, ImageFont
    from io import  BytesIO

    img = Image.new('RGB', (270, 30), color=get_random_color())

    draw = ImageDraw.Draw(img)
    kumo_font = ImageFont.truetype('static/font/kumo.ttf', size=20, )

    valid_code_str = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((i*50, 5), random_char, get_random_color(), font=kumo_font)
        valid_code_str += random_char

    draw.line()
    draw.point()

    width = 270
    height = 30
    for i in range(10):
        x1 = random.randint(0,width)
        x2 = random.randint(0,width)
        y1 = random.randint(0,height)
        y2 = random.randint(0,height)
        draw.line((x1,y1,x2,y2), fill=get_random_color())

    for i in range(100):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())
    request.session["valid_code_str"] = valid_code_str

    f = BytesIO()

    img.save(f, 'png')

    data = f.getvalue()
    return data
