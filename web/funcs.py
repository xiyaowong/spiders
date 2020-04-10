import re

from flask import current_app
from requests.exceptions import ConnectionError, ConnectTimeout, Timeout

from ..extractor import (acfun, baidutieba, bilibili, changya, douyin, haokan,
                         ku6, kuaishou, kugou, kuwo, lizhiFM, lofter, music163,
                         open163, pearvideo, pipigaoxiao, pipix, qianqian,
                         qingshipin, qqmusic, quanminkge, qutoutiao, sing5,
                         sohuTV, ted, tudou, wechat_article_cover, weibo,
                         weishi, xiaokaxiu, xinpianchang, zhihu_video,
                         zuiyou_voice)
from . import response

URL_PATTERN = r"https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\.[-A-Za-z]+[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]"


def extract(url: str):  # pylint: disable=too-many-statements
    url = re.findall(URL_PATTERN, url)
    if not url:
        return response(404, msg="无法匹配到链接")
    url = url[0]

    if "acfun" in url:
        f = acfun
    elif "tieba" in url:
        f = baidutieba
    elif "bili" in url:
        f = bilibili
    elif "changya" in url:
        f = changya
    elif "douyin" in url:
        f = douyin
    elif "haokan" in url:
        f = haokan
    elif "ku6" in url:
        f = ku6
    elif "chenzhongtech" in url or "kuaishou" in url:
        f = kuaishou
    elif "kugou" in url:
        f = kugou
    elif "kuwo" in url:
        f = kuwo
    elif "lizhi" in url:
        f = lizhiFM
    elif "lofter" in url:
        f = lofter
    elif "music.163" in url:
        f = music163
    elif "open.163" in url:
        f = open163
    elif "pearvideo" in url:
        f = pearvideo
    elif "ippzone" in url:
        f = pipigaoxiao
    elif "pipix" in url:
        f = pipix
    elif "music.taihe" in url:
        f = qianqian
    elif "qingshipin" in url:
        f = qingshipin
    elif "y.qq" in url:
        f = qqmusic
    elif "kg" in url:
        f = quanminkge
    elif "qutoutiao" in url:
        f = qutoutiao
    elif "5sing" in url:
        f = sing5
    elif "weibo" in url:
        f = weibo
    elif "weishi" in url:
        f = weishi
    elif "xiaokaxiu" in url:
        f = xiaokaxiu
    elif "xinpianchang" in url:
        f = xinpianchang
    elif "zhihu" in url:
        f = zhihu_video
    elif "zuiyou" in url:
        f = zuiyou_voice
    elif "sohu" in url:
        f = sohuTV
    elif "ted" in url:
        f = ted
    elif "tudou" in url:
        f = tudou
    else:
        return response(code=400, msg="不支持的链接")

    try:
        data = f.get(url)  # type: dict
        # 删除值为空的键
        for key, value in data.copy().items():
            if not value:
                data.pop(key)
        return response(data=data, msg=data.get("msg"))
    except Exception as e:
        current_app.logger.error(e)
        return response(500, error=e, msg="服务器错误")
