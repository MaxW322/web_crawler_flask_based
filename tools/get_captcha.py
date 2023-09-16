from io import BytesIO
from random import choices
from captcha.image import ImageCaptcha
from flask import make_response
from PIL import Image


def gen_captcha(content="0123456789"):
    """生成图片对象"""
    image = ImageCaptcha()
    # 获取字符串
    captcha_text = "".join(choices(content, k=4))
    # 生成图片
    captcha_image = Image.open(image.generate(captcha_text))
    img = captcha_image.resize((122, 38), Image.ANTIALIAS)
    return captcha_text, img


# 生成验证码
def get_captcha_code_and_content():
    code, image = gen_captcha()
    out = BytesIO()
    image.save(out, "png")
    out.seek(0)
    content = out.read()  # 读取图片的二进制数据做响应体
    return code, content


if __name__ == '__main__':
    code, content = get_captcha_code_and_content()
    print(code, content)
