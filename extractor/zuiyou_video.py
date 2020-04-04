import json
from urllib.parse import urlparse

import requests
import re

def get(url: str) -> dict:
    """
    text、videos
    """
    data = {}
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "share.izuiyou.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    re_title = r'<div class="SharePostCard__content"><span.*?</span>(.*?)</div>'
    re_video = r'<video src="(.*?)".*?></video>'

    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            title = re.findall(re_title, rep.text)
            video = re.findall(re_video, rep.text)
            if title:
                data["title"] = title[0]
            if video:
                data["videos"] = video
        else:
            data["msg"] = "失败"

    return data


if __name__ == "__main__":
    url = "https://share.izuiyou.com/detail/147486886?zy_to=applink&to=applink"
    print(get(url))
