# -*- coding: utf-8 -*-
import time

import requests
import hashlib


class DouyinFontMap:
    douyin_font_map = {
        '58882': '1', '58883': '0', '58884': '3', '58885': '2', '58886': '4', '58887': '5', '58888': '6',
        '58889': '9', '58890': '7', '58891': '8', '58892': '4', '58893': '0', '58894': '1', '58895': '5',
        '58896': '2', '58897': '3', '58898': '6', '58899': '7', '58900': '8', '58901': '9', '58902': '0',
        '58903': '2', '58904': '1', '58905': '4', '58906': '3', '58907': '5', '58908': '7', '58909': '8',
        '58910': '9', '58911': '6'}

    @classmethod
    def font_convert(cls, temp):
        """
        :param temp: 加密的字符列表
        :return: 十进制的数字
        """
        fonts = []
        for i in temp:
            # 去除 Unicode 字符两端的空格
            t = i.strip()
            # 如果是纯空格字符串，就跳过
            if not t:
                continue
            # 如果是 . 和 w 直接添加进列表
            elif t in [".", "w"]:
                fonts.append(t)
            # 如果是 unicode，就经过 font_map 得到 value，在添加进列表
            else:
                fonts.append(cls.douyin_font_map[str(ord(t))])
        result = "".join(fonts)
        if 'w' in result:
            return int(float(result.split('w')[0]) * 10000)
        return int(result)


def get_douyin_signature(params):
    """
    :param params: {uid: 用户长id, tac: 从博主个人主页html源码中获取}
    :return: _signature 加密参数
    """
    # 本地 nodejs 服务器，提供 _signature 参数的生成
    local_server = 'http://127.0.0.1:8000/douyin'
    try:
        res = requests.get(local_server, params=params)
    except:
        print("本地 nodejs 服务器异常，获取 _signature 失败！")
        return
    return res.text


def get_md5(url):
    """
    :param url: url
    :return: md5加密串
    """
    if isinstance(url, str):
        url = url.encode()
    return hashlib.md5(url).hexdigest()
