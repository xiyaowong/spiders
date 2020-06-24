import re

from flask import current_app

from extractor import (acfun, baidutieba, bilibili, changya, douyin, haokan,
                       ku6, kuaishou, kugou, kuwo, lizhiFM, lofter, migu_music,
                       momo, music163, open163, pearvideo, pic58, pipigaoxiao,
                       pipix, qianqian, qingshipin, qqmusic, quanminkge,
                       qutoutiao, sing5, sohuTV, ted, tuchong, tudou, weibo,
                       weishi, xiaokaxiu, xinpianchang, zhihu_video,
                       zuiyou_voice)

from web import response



crawlers = {
    'acfun': acfun,
    'tieba': baidutieba,
    'bili': bilibili,
    'changya': changya,
    'douyin': douyin,
    'haokan': haokan,
    'ku6': ku6,
    'chenzhongtech': kuaishou,
    'kuaishou': kuaishou,
    'kugou': kugou,
    'kuwo': kuwo,
    'lizhi': lizhiFM,
    'lofter': lofter,
    'music.163': music163,
    'open.163': open163,
    'pearvideo': pearvideo,
    'ippzone': pipigaoxiao,
    'pipix': pipix,
    'music.taihe': qianqian,
    'qingshipin': qingshipin,
    'y.qq': qqmusic,
    'kg': quanminkge,
    'qutoutiao': qutoutiao,
    '5sing': sing5,
    'weibo': weibo,
    'weishi': weishi,
    'xiaokaxiu': xiaokaxiu,
    'xinpianchang': xinpianchang,
    'zhihu': zhihu_video,
    'zuiyou': zuiyou_voice,
    'sohu': sohuTV,
    'ted': ted,
    'tudou': tudou,
    'momo': momo,
    'music.migu': migu_music,
    '58pic': pic58,
    'tuchong': tuchong
}


def extract(url: str):  # pylint: disable=too-many-statements
    try:
        url = re.findall(
            r"https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\.[-A-Za-z]+[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", url)
        if not url:
            return response(404, msg="无法匹配链接")
        url = url[0]

        data = None
        for c_name, c_func in crawlers.items():
            if c_name in url:
                data = c_func.get(url)  # type: dict
                break
        if data is not None:
            # 删除值为空的键
            for key, value in data.copy().items():
                if not value:
                    data.pop(key)
            return response(data=data, msg=data.get("msg"))
        else:
            return response(404, msg="不支持的链接")
    except Exception as e:
        current_app.logger.error(e)
        current_app.logger.exception(e)
        return response(500, error=e, msg="服务器错误")
