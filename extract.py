#! python
import argparse

from extractor import *
from utils import download

# 乱七八糟，奇奇怪怪，凑合用（笑
tips = """
 _______  _______ _________ ______   _______  _______
(  ____ \(  ____ )\__   __/(  __  \ (  ____ \(  ____ )
| (    \/| (    )|   ) (   | (  \  )| (    \/| (    )|
| (_____ | (____)|   | |   | |   ) || (__    | (____)|
(_____  )|  _____)   | |   | |   | ||  __)   |     __)
      ) || (         | |   | |   ) || (      | (\ (
/\____) || )      ___) (___| (__/  )| (____/\| ) \ \__
\_______)|/       \_______/(______/ (_______/|/   \__/

爬取并下载部分资源@wongxy
========================================
bilibili(哔哩哔哩) | 封面、视频
changya(唱鸭) | 音频
douyin(抖音) | 无水印视频
kugou(酷狗) | 音频
kuwo(酷我) | 音频
lizhiFM(荔枝FM) | 音频
music163(网易云音乐) | 音频
qqmusic(QQ音乐) | 音频
pipigaoxiao(皮皮搞笑) | 无水印视频
quanminkge(全民K歌) | 音频或视频
weibo(微博) | 视频
weishi(微视) | 无水印视频
zhihu(知乎) | 视频
zuiyou(最右) | 音频(语音帖评论)
qianqian(千千音乐) | 音频
5sing(5sing) | 音频
pipix(皮皮虾) | 无水印视频
qingshipin(轻视频) | 无水印视频
qutoutiao(趣头条) | 视频
ku6(酷6网) | 视频
lofter(乐乎) | 视频
open163(网易公开课) | 免费视频
xinpianchang(新片场) | 视频
baidutieba(百度贴吧) | 视频
kuaishou(快手) | 无水印视频、长图视频
acfun(AcFun弹幕网) | 视频
haokan(百度好看视频) | 视频
pearvideo(梨视频) | 视频
xiaokaxiu(小咖秀) | 无水印视频
========================================
"""


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
    elif "chenzhongtech" in url:
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
    else:
        return {"msg": "链接无法解析"}
    return f.get(url)


parser = argparse.ArgumentParser(description=tips)
parser.add_argument("-url", type=str, default=None, help="需要解析的链接")
args = parser.parse_args()

url = args.url  # type: str
if url is None:
    print(tips)
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

if text:
    print(text)

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
