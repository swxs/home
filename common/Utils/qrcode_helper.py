# -*- coding: utf-8 -*-
import os
import qrcode
import io
import base64


# 将链接转为二维码输出
def get_matrix_img_by_param(content, img_type='png', box_size=5, border=1, img_name='default'):
    box_size = int(box_size)
    box_size = 50 if box_size > 50 else box_size
    q = qrcode.main.QRCode(box_size=box_size, border=border)
    q.add_data(content)
    m = q.make_image()
    # buf = io.StringIO()
    buf = io.BytesIO()
    m.save(buf, img_type)
    data = base64.encodebytes(buf.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    return src.replace("\n", "")


# 将连接转为二维码并储存
def save_matrix_img_by_param(content, path, img_type='png', box_size=5, border=1, img_name='default'):
    box_size = int(box_size)
    box_size = 50 if box_size > 50 else box_size
    q = qrcode.main.QRCode(box_size=box_size, border=border)
    q.add_data(content)
    m = q.make_image()
    image_path = "{0}.{1}".format(path, img_type)
    m.save(image_path, img_type)
    return image_path
