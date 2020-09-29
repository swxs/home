# -*- coding: utf-8 -*-

import os
import io
import re
import qrcode
import base64
from PIL import Image
from pyzbar.pyzbar import decode as qrdecode


class Helper_image():
    def __init__(self) -> None:
        pass

    def __enter__(self, path):
        self.path = path
        return self

    def __exit__(self):
        pass

    @classmethod
    def image_to_base64(cls, img):
        """
        简介
        ----------
        将图片转化为base64格式文本
        """
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        data = base64.b64encode(buf.getvalue())
        return f'data:image/png;base64,{data}'.replace("\n", "")

    @classmethod
    def base64_to_image(cls, src):
        """
        简介
        ----------
        将base64格式文本转化为图片
        """
        data = re.sub('^data:image/.+;base64,', '', src)
        byte_data = base64.b64decode(data)
        image_data = io.BytesIO(byte_data)
        return Image.open(image_data)

    @classmethod
    def encode_qrcode(cls, data, box_size=5, border=1):
        """
        简介
        ----------
        将数据转化为二维码
        """
        box_size = int(box_size)
        box_size = 50 if box_size > 50 else box_size
        q = qrcode.main.QRCode(box_size=box_size, border=border)
        q.add_data(data)
        return q.make_image()

    @classmethod
    def decode_qrcode(cls, img):
        """
        简介
        ----------
        将二维码转化为数据
        """
        result = qrdecode(img)
        for _r in result:
            if _r.type == "QRCODE":
                return result[0].data.decode()

    @classmethod
    def save(cls, img, filepath):
        file, ext = os.path.splitext(filepath)
        img.save(file, ext[1:])
