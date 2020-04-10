from flask import Flask, request

from . import funcs

from . import response


def home():
    data = "This is Home Page"
    return response(data=data)


def extract():
    if "url" not in request.values:
        return response(404, msg="the arg 'url' is reqeuired!")
    url = request.values["url"]
    return funcs.extract(url)


def allow():
    return r"(acfun|tieba|bili|changya|douyin|haokan|ku6|chenzhongtech|kuaishou|kugou|kuwo|lizhi|lofter|music\.163|open\.163|pearvideo|ippzone|pipix|music\.taihe|qingshipin|y\.qq|kg|qutoutiao|5sing|weibo|weishi|xiaokaxiu|zhihu|zuiyou|sohu|ted|tudou)"


def desc():
    data = [["哔哩哔哩", "封面、视频"],
            ["唱鸭", "音频"],
            ["抖音", "无水印视频"],
            ["酷狗", "音频"],
            ["酷我", "音频"],
            ["荔枝FM", "音频"],
            ["网易云音乐", "音频"],
            ["QQ音乐", "音频"],
            ["皮皮搞笑", "无水印视频"],
            ["全民K歌", "音频&视频"],
            ["微博", "视频"],
            ["微视", "无水印视频"],
            ["知乎", "视频"],
            ["最右", "音频(语音帖评论)"],
            ["千千音乐", "音频"],
            ["5sing", "音频"],
            ["皮皮虾", "无水印视频"],
            ["轻视频", "无水印视频"],
            ["趣头条", "视频"],
            ["酷6网", "视频"],
            ["乐乎", "视频"],
            ["网易公开课", "视频(免费)"],
            ["新片场", "视频"],
            ["百度贴吧", "视频"],
            ["快手", "无水印视频、长图视频"],
            ["AcFun弹幕网", "视频"],
            ["百度好看视频", "视频"],
            ["梨视频", "视频"],
            ["小咖秀", "无水印视频"],
            ["搜狐视频", "视频"],
            ["土豆视频", "视频(免费电视剧等)"],
            ["TED", "视频"],
            ]
    return response(data=data)


def init_app(app: Flask) -> None:
    app.add_url_rule("/", "home", home)
    app.add_url_rule("/extract/", "extract", extract)
    app.add_url_rule("/extract/allow/", "allow", allow)
    app.add_url_rule("/extract/desc/", "desc", desc)
