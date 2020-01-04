import functools
import os
import re
import requests
import traceback
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import current_app
from flask import session
from flask_mail import Message
from super_bbs.core.extensions import mail, redis_store
from super_bbs.core.basehandler import LogicError, AuthError, BaseError, VerifyError
from super_bbs.config import BASE_DIR
from super_bbs.constants import release_lock_script


class HttpClient(object):

    def __init__(self, cookies=None):
        self.client = requests
        self.cookies = cookies

    def get(self, url, params=None, cookies=None):
        if cookies:
            cookies.update(self.cookies)
        else:
            cookies = self.cookies
        try:
            ret = self.client.get(url=url, params=params, cookies=cookies)
            if ret.status_code not in [200, 201]:
                raise BaseError(f'request {url}, params {params} error, http code is {ret.status_code}')
            return ret
        except Exception:
            err = traceback.format_exc()
            raise BaseError(f'request error: {err}')

    def post(self, url, data=None, cookies=None):
        if cookies:
            cookies.update(self.cookies)
        else:
            cookies = self.cookies
        try:
            ret = self.client.post(url=url, json=data, cookies=cookies)
            if ret.status_code not in [200, 201]:
                raise BaseError(f'request {url}, data {data} error, http code is {ret.status_code}')
            return ret
        except Exception:
            err = traceback.format_exc()
            raise BaseError(f'request error: {err}')


def login_required(admin=False):
    def func_wrapper(func):
        @functools.wraps(func)
        def _func_wrapper(cls, *args, **kwargs):
            if not session.get('is_login'):
                raise AuthError('登录后才可以操作哦')
            if admin:
                if session.get('role_id') != 1:
                    raise VerifyError('没有操作权限')

            return func(cls, *args, **kwargs)

        return _func_wrapper

    return func_wrapper


def need_params(*params, **type_params):
    def dec(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            for arg in params:
                if getattr(self.input, arg) is None:
                    raise LogicError('需要:%s 参数' % arg)
                if getattr(self.input, arg) == '':
                    raise LogicError('参数:%s 不能为空' % arg)
            for k, _type in type_params.items():
                if getattr(self.input, k) is None:
                    raise LogicError('需要:%s 参数' % k)
                if getattr(self.input, k) == '':
                    raise LogicError('参数:%s 不能为空' % k)
                if not isinstance(getattr(self.input, k), _type):
                    raise LogicError('参数 "%s" 类型应该是: %s' % (k, _type))

            return func(self, *args, **kwargs)

        return wrapper

    return dec


def generate_check_code(width=120, height=30, char_length=5, font_name='Rocko.ttf', font_size=28):
    font_file = os.path.join(BASE_DIR, font_name)

    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


def send_mail(body, title, recipients):
    msg = Message(
        title,
        recipients=recipients
    )
    msg.body = body
    msg.html = "<h1>big</h1>"
    mail.send(msg)
    current_app.logger.info('mail send to {0}'.format(','.join(recipients)))


def release_redis_lock(lock_key_name, lock_value):
    script_client = redis_store.register_script(release_lock_script)
    return script_client(keys=[lock_key_name], args=[lock_value])
