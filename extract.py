import re

from prettytable import PrettyTable
from requests.exceptions import ConnectTimeout, ConnectionError

from extractor import (acfun, baidutieba, bilibili, changya, douyin, haokan,
                       ku6, kuaishou, kugou, kuwo, lizhiFM, lofter, music163,
                       open163, pearvideo, pipigaoxiao, pipix, qianqian,
                       qingshipin, qqmusic, quanminkge, qutoutiao, sing5,
                       sohuTV, ted, tudou, wechat_article_cover, weibo, weishi,
                       xiaokaxiu, xinpianchang, zhihu_video, zuiyou_voice, tuchong)

from utils import download

# 乱七八糟，奇奇怪怪，凑合用（笑
logo = r"""
 _______  _______ _________ ______   _______  _______
(  ____ \(  ____ )\__   __/(  __  \ (  ____ \(  ____ )
| (    \/| (    )|   ) (   | (  \  )| (    \/| (    )|
| (_____ | (____)|   | |   | |   ) || (__    | (____)|
(_____  )|  _____)   | |   | |   | ||  __)   |     __)
      ) || (         | |   | |   ) || (      | (\ (
/\____) || )      ___) (___| (__/  )| (____/\| ) \ \__
\_______)|/       \_______/(______/ (_______/|/   \__/"""
platforms = [
    ["哔哩哔哩", "封面、视频"],
    ["唱鸭", "音频"],
    ["抖音", "无水印视频"],
    ["酷狗", "音频"],
    ["酷我", "音频"],
    ["荔枝FM", "音频"],
    ["网易云音乐", "音频、mv、视频"],
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
    ["图虫", "图片"],
]
table = PrettyTable(["支持平台", "支持内容"])
for platform in platforms:
    table.add_row(platform)
print(logo)
print("""
╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮
│ @wongxy github.com/xiyaowong │
╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯""")
print("爬取并下载部分资源")
print(table)


def get(url=None):
    if url is None:
        url = input("请输入链接：")

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
        return {"msg": "链接无法解析"}
    return f.get(url)


def spider(url):
    data = get(url)

    title = data.get("title")
    author = data.get("author")
    audioName = data.get("audioName")
    videoName = data.get("videoName")
    imgs = data.get("imgs")
    audios = data.get("audios")
    videos = data.get("videos")
    text = data.get("text")
    msg = data.get("msg")

    if msg:
        print(msg)
        print()

    if text:
        print(text)
        print()

    if imgs:
        for img in imgs:
            download(img, file_type="jpg")

    if audios:
        file_name = (audioName or "") + "-" + (author or "")
        if file_name == "-":
            file_name = None
        for audio in audios:
            download(audio, file_name=file_name, file_type="mp3")

    if videos:
        file_name = (videoName or title or "")
        if file_name == "":
            file_name = None
        for video in videos:
            download(video, file_name=file_name, file_type="mp4")


if __name__ == "__main__":
    while True:
        try:
            what = input("输入链接http开头(输入任意不包含链接的内容就能退出)：")

            urls = re.findall(
                r"https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\.[-A-Za-z]+[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", what)
            if not urls:
                print("bye~")
                break
            print(f"""
    ╭━━━━━━━━━━━━━╮
    │ 一共{len(urls)}个链接 │
    ╰━━━━━━━━━━━━━╯
            """)
            for idx, url in enumerate(urls):
                print(f"正在解析第{idx+1}个链接【{url}】")
                spider(url)
                print()
        except RuntimeError:
            print("运行超时")
        except ConnectTimeout:
            print("网络连接超时")
        except ConnectionError:
            print("连接错误")
