import os
import re
from datetime import datetime
from queue import Queue
from threading import Thread

import utils
from extractor import (acfun, baidutieba, bilibili, changya, douyin, haokan,
                       ku6, kuaishou, kugou, kuwo, lizhiFM, lofter, migu_music,
                       momo, music163, open163, pearvideo, pic58, pipigaoxiao,
                       pipix, qianqian, qingshipin, qqmusic, quanminkge,
                       qutoutiao, sing5, sohuTV, ted, tuchong, tudou, weibo,
                       weishi, xiaokaxiu, xinpianchang, zhihu_video,
                       zuiyou_voice)
from misc import printTips

here = os.path.abspath(os.path.dirname(__file__))

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


class Task:
    def __init__(self, url, save_path='', file_name=None, file_type='unknown'):
        self.url = url
        self.save_path = save_path
        self.file_name = file_name or str(datetime.now())
        self.file_type = file_type


def data2tasks(data: dict) -> list:
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
    tasks = []
    if imgs:
        img_tasks = [Task(img, 'download/images', file_type='jpg') for img in imgs]
        tasks.extend(img_tasks)
    if audios:
        file_name = (audioName or "") + "-" + (author or "")
        audio_tasks = [Task(audio, 'download/audios', file_name=file_name, file_type='mp3') for audio in audios]
        tasks.extend(audio_tasks)
    if videos:
        file_name = (videoName or title or "")
        video_tasks = [Task(video, 'download/videos', file_name=file_name, file_type='mp4') for video in videos]
        tasks.extend(video_tasks)
    return tasks


@utils.retry(2)
def dl(dl_queue: Queue):
    while not dl_queue.empty():
        task = dl_queue.get()  # type: Task
        utils.download(file_url=task.url,
                       save_path=task.save_path,
                       file_name=task.file_name,
                       file_type=task.file_type)


def get_data(url):
    for c_name, c_func in crawlers.items():
        if c_name in url:
            data = c_func.get(url)
            print(data)
            return data
    print(f'链接【\033[31m{url}\033[0m】不支持')
    return None


@utils.retry(2)
def parse_urls(text: str) -> list:
    urls = re.findall(
        r"https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]\.[-A-Za-z]+[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", text)
    return urls


if __name__ == "__main__":
    printTips()
    while True:
        what = input("输入链接http开头(输入任意不包含链接的内容就能退出)：")
        urls = parse_urls(what)
        if not urls:
            print("bye~")
            break
        print(f"""
╭━━━━━━━━━━━━━╮
│ 一共{len(urls)}个链接 │
╰━━━━━━━━━━━━━╯
        """)
        all_task = []
        for idx, url in enumerate(urls):
            print(f"正在解析第{idx+1}个链接【{url}】")
            data = get_data(url)
            if data:
                all_task.extend(data2tasks(data))

        queue = Queue(maxsize=100)
        for t in all_task:
            queue.put(t)

        print()
        print(f'{len(all_task)} tasks!')
        print()
        ts = [Thread(target=dl, args=(queue, )) for _ in range(min(len(all_task), 6))]
        for t in ts:
            t.start()

        for t in ts:
            t.join()
