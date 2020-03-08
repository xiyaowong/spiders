from flask import Flask
from flask import request
from flask import jsonify
from . import response


def home():
    data = "This is Home Page"
    return response(data=data)


def extract():
    if "url" not in request.values:
        return response(404, message="the arg 'url' is reqeuired!")
    url = request.values["url"]
    return _extract(url)


def allow():
    return r"(bili|changya|kugou|douyin|kuwo|lizhi|music\.163|ippzone|kg\.qq|weibo|weishi|zhihu|zuiyou)"


def _extract(url: str):
    import re
    from requests.exceptions import ConnectionError, ConnectTimeout, Timeout
    from ..extractor import \
        (
            bilibili, changya, douyin, kugou, kuwo, lizhiFM, music163, pipigaoxiao,
            quanminkge, weibo, weishi, zhihu_video, zuiyou_voice
        )
    url = re.findall(
        r"https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\.[-A-Za-z]+[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", url)
    if not url:
        return response(404, message="无法匹配到链接")
    url = url[0]
    try:
        if "bili" in url:
            data = bilibili.get(url)
        elif "changya" in url:
            data = changya.get(url)
        elif "kugou" in url:
            data = kugou.get(url)
        elif "kuwo" in url:
            data = kuwo.get(url)
        elif "lizhi" in url:
            data = lizhiFM.get(url)
        elif "music.163" in url:
            data = music163.get(url)
        elif "ippzone" in url:
            data = pipigaoxiao.get(url)
        elif "kg" in url and "qq" in url:
            data = quanminkge.get(url)
        elif "weibo" in url:
            data = weibo.get(url)
        elif "weishi" in url:
            data = weishi.get(url)
        elif "zhihu" in url:
            data = zhihu_video.get(url)
        elif "zuiyou" in url:
            data = zuiyou_voice.get(url)
        elif "douyin" in url:
            data = douyin.get(url)
        else:
            return response(400, message="不支持的链接！")
    except (ConnectTimeout, ConnectTimeout, Timeout):
        return response(500)

    # 删除值为空的键
    for key, value in data.copy().items():
        if not value:
            data.pop(key)

    return response(data=data)



def init_app(app: Flask) -> None:
    app.add_url_rule("/", "home", home)
    app.add_url_rule("/extract/", "extract", extract)
    app.add_url_rule("/extract/allow/", "allow", allow)

