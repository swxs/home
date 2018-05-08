#encoding=utf8

import re
import os
import math
import json
import codecs
import shutil
import hashlib
import datetime
from tornado.util import ObjectDict
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import numpy as np
import pandas as pd
import tornado.template
try:
    Period = pd._period.Period
except AttributeError:
    Period = pd._libs.period.Period
import settings
from const import undefined

tmpl_loader = tornado.template.Loader("./templates")
def render_to_string(tmpl_file, **adict):
    return tmpl_loader.load(tmpl_file).generate(**adict)


from HTMLParser import HTMLParser
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def touch_file(file_name):
    if not os.path.exists(file_name):
        file_path = os.path.dirname(file_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file(file_name, 'wb').write('')

def cutstring(str='', width=10, charset='unicode', addchar='...', br_num=0, line_num=0):
    oldstr = str
    oldaddchar = addchar
    if br_num != 0:
        str_br = u'<br>'
    if type(oldstr).__name__ != 'unicode':
        try:
            oldstr = oldstr.decode(charset)
        except:
            pass

    if oldaddchar and type(oldaddchar).__name__ != 'unicode':
        oldaddchar = oldaddchar.decode(charset)

    index = 0
    usedwidth = 0
    br_index_list = []
    for i in oldstr:
        if ord(i) < 128:
            usedwidth = usedwidth + 1
            if br_num != 0 and index % br_num == 0 and index != 0:
                br_index_list.append(index)
        else:
            usedwidth = usedwidth + 2
            if br_num != 0 and index % (br_num / 2) == 0 and index != 0:
                br_index_list.append(index)
        if usedwidth > width:
            break
        if usedwidth == width:
            if not addchar:
                pass
            elif index == len(oldstr) - 1:
                pass
            else:
                break
        index = index + 1

    if br_num != 0:
        #记录取到哪
        str_idx = 0
        line_count = 0
        newstr = u''
        #循环取每行数据并加上换行
        for idx in br_index_list:
            if line_count == line_num - 1:
                newstr += oldstr[str_idx:idx]
            else:
                newstr += oldstr[str_idx:idx] + str_br
            str_idx = idx
            line_count = line_count + 1
        #取最后剩余不足一行的部分
        if line_count < line_num:
            #需要分行
            if len(br_index_list) > 0:
                if br_index_list[0] % br_num == 0:
                    newstr = newstr + oldstr[str_idx:width]
                else:
                    newstr = newstr + oldstr[str_idx:width / 2]
            #无需分行
            else:
                newstr = oldstr
        #补上...
        if index < len(oldstr):
            newstr = newstr + oldaddchar
    elif index == len(oldstr):
        newstr = oldstr
    elif index < len(oldstr):
        newstr = oldstr[0:index] + oldaddchar

    if charset != 'unicode':
        try:
            newstr = newstr.encode(charset)
        except:
            pass

    return newstr


def get_matrix_img_by_param(content, img_type='png', box_size=5, border=1, img_name='default'):
    import qrcode
    if box_size > 200:
        raise Exception("box_size [%s] too big, max %s" % (box_size, 200))
    q = qrcode.main.QRCode(box_size=box_size, border=border)
    q.add_data(content)
    m = q.make_image()
    return m._img


def get_matrix_img_stream_by_param(content, img_type='png', box_size=5, border=1):
    img = get_matrix_img_by_param(content, img_type, box_size, border)
    mstream = StringIO.StringIO()
    img.__name__ = "xjxjxj.png"
    img.save(mstream, img_type)
    return mstream


def my_urlencode(astring):
    from urllib import urlencode
    return urlencode({'a': astring})[2:]


def remove_dir(Dir):
    if os.path.isdir(Dir):
        paths = os.listdir(Dir)
        for path in paths:
            filePath = os.path.join(Dir, path)
            if os.path.isfile(filePath):
                try:
                    os.remove(filePath)
                except os.error:
                    pass
            elif os.path.isdir(filePath):
                if filePath[-4:].lower() == ".svn".lower():
                    continue
                shutil.rmtree(filePath, True)
    os.rmdir(Dir)
    return True


def get_verify_code(*args):
    import settings
    args_str = ''.join([str(x) for x in args])
    args_str += settings.SECRET_KEY
    return hashlib.md5(args_str).hexdigest()


def obj2objdict(obj):
    if isinstance(obj, dict):
        new_obj = ObjectDict()
        for k, v in obj.iteritems():
            new_obj[k] = obj2objdict(v)
        return new_obj
    elif isinstance(obj, (list, tuple)):
        new_obj = []
        for item in obj:
            new_obj.append(obj2objdict(item))
        return new_obj
    elif isinstance(obj, set):
        new_obj = set()
        for item in obj:
            new_obj.add(obj2objdict(item))
        return new_obj
    else:
        return obj


def update_option(orig_option, new_option):
    for key, value in new_option.iteritems():
        if key in orig_option:
            orig_value = orig_option[key]
            if isinstance(orig_value, dict):
                update_option(orig_value, value)
            else:
                orig_option[key] = value
        else:
            orig_option[key] = value


def change_type(obj):
    if isinstance(obj, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
        return str(int(obj))
    elif isinstance(obj, (np.float, np.float16, np.float32, np.float64)):
        if math.isnan(obj):
            return "N/A"
        elif np.isinf(obj):
            return "Inf"
        else:
            return float(obj)
    else:
        return obj


def change_data_filter_type(obj):
    if isinstance(obj, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
        return str(int(obj))
    elif isinstance(obj, (np.float, np.float16, np.float32, np.float64)):
        if math.isnan(obj):
            return
        elif np.isinf(obj):
            return
        else:
            return float(obj)
    else:
        return obj


def encode_data(obj):
    if isinstance(obj, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
        return str(int(obj))
    elif isinstance(obj, (np.float, np.float16, np.float32, np.float64)):
        if math.isnan(obj):
            return "N/A"
        elif np.isinf(obj):
            return "Inf"
        else:
            return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.datetime64):
        try:
            return pd.to_datetime(str(obj)).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return "N/A"
    elif isinstance(obj, (datetime.datetime, Period)):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return obj


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
            return int(obj)
        elif isinstance(obj, (np.float, np.float16, np.float32, np.float64)):
            if math.isnan(obj):
                return "N/A"
            elif np.isinf(obj):
                return "Inf"
            else:
                return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, Period):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return super(MyEncoder, self).default(obj)


def encode_unicode(string):
    if not string:
        return
    codecs.encode(string, 'raw_unicode_escape').decode('utf-8')


def get_password(password):
    return hashlib.md5(settings.SECRET_KEY + password).hexdigest()
