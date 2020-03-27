# @wongxy
import re

import requests


def get(url: str) -> dict:
    """
    title、imgs、videos
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
        "Cookie": "did=web_66d3f43c55744795a6210847eff2074e; didv=1585296414000",
    }
    re_title = r'<meta name="description" itemprop="description" content="(.*?)">'
    re_video = r';srcNoMark&#34;:&#34;(https://.*?\.mp4)'
    re_img = r'&#34;path&#34;:&#34;(.*?\.jpg)&#34;'

    rep = requests.get(url, headers=headers, timeout=10)
    if rep.status_code != 200:
        return {"msg": f"{rep.status_code}获取失败"}

    title = re.findall(re_title, rep.text)
    video = re.findall(re_video, rep.text)
    img = re.findall(re_img, rep.text)
    if title:
        data["title"] = title[0]
    if video:
        data["videos"] = video
# https://js2.a.yximgs.com/ufile/atlas/NTE5Njg3MjUyMDE5MTk4MTM4OF8xNTg0NzkyNzI4MjAy_15.jpg
    if img:
        data["imgs"] = ["https://js2.a.yximgs.com" +
                        i for i in img[:-1]]  # 最后一张是水印
    return data


if __name__ == "__main__":
    print(get(input("url: ")))
