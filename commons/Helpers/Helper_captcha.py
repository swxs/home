# encoding:utf-8
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import os
import io


img_captcha_prefix = 'img_captcha_'


class RandomChar:
    """用于随机生成字符"""

    @staticmethod
    def Unicode():
        cnCharacters = "123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMLNOPQRSTUVWXYZ"
        chrLength = len(cnCharacters) - 1
        return cnCharacters[random.randint(0, chrLength)]


class ImageChar:
    def __init__(
        self,
        fontColor=(0, 0, 0),
        size=(100, 40),
        fontPath='./TAHOMABD.TTF',
        bgColor=(255, 255, 255),
        fontSize=22,
    ):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize, encoding='unic')
        self.image = Image.new('RGB', size, bgColor)

    def rotate(self):
        self.image.rotate(random.randint(0, 30), expand=0)

    def drawText(self, pos, txt, fill):
        draw = ImageDraw.Draw(self.image)
        draw.text(pos, txt, font=self.font, fill=fill)
        del draw

    def randRGB(self, base=0):
        return (random.randint(base, 255), random.randint(base, 255), random.randint(base, 255))

    def randPoint(self):
        (width, height) = self.size
        return (random.randint(0, width * 2) - width / 2, random.randint(0, height * 2) - height / 2)

    def randLine(self, num):
        draw = ImageDraw.Draw(self.image)
        for i in range(0, num):
            draw.line([self.randPoint(), self.randPoint()], self.randRGB(), width=random.randint(0, 3))
        del draw

    def randChinese(self, num):
        gap = 3
        start = 1
        uchr = ''
        for i in range(0, num):
            tmpchr = RandomChar().Unicode()
            uchr = uchr + tmpchr
            x = start + self.fontSize * i + random.randint(0, gap) + gap * i
            self.drawText((x, random.randint(-5, 5)), tmpchr, self.randRGB())
            self.rotate()
        self.randLine(18)
        return uchr

    def save(self, path, format=None):
        self.image.save(path, format=format)


class ImageChinese(ImageChar):
    def __init__(
        self,
        fontColor=(0, 0, 0),
        size=(110, 40),
        fontPath='./msyh.TTF',
        bgColor=(255, 255, 255),
        fontSize=22,
    ):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize, encoding='unic')
        self.image = Image.new('RGB', size, bgColor)

    def drawText(self, pos, txt, fill):
        img = Image.new('RGBA', (40, 40))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), txt, font=self.font, fill=fill)
        img = img.rotate(random.randint(-30, 30), expand=True, center=(20, 20))
        self.image.paste(img, pos, img.getchannel(3))

    def randChinese(self, num):
        gap = 3
        start = 1
        uchr = ''
        self.randLine(5)
        for i in range(0, num):
            head = random.randint(0xB0, 0xD7)
            # 在head区号为55的那一块最后5个汉字是乱码,忽略了body[0xfa,0xfe]的部分
            body = random.randint(0xA1, 0xF9)
            tmpchr = bytes([head, body]).decode('gb2312')
            uchr = uchr + tmpchr
            x = start + self.fontSize * i + random.randint(0, gap) + gap * i
            self.drawText((x, random.randint(-3, 3)), tmpchr, self.randRGB(30))
        self.randLine(5)
        return uchr
