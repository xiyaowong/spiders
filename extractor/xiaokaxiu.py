# @wongxy
import time
from hashlib import md5
from urllib.parse import urlparse, parse_qs

import requests


def get(url: str) -> dict:
    """
    title、videos
    """
    data = {}

    try:
        qs = parse_qs(urlparse(url).query)
        video_id = qs["id"][0]
    except KeyError:
        return {"msg": "无法匹配视频id"}

    timestamp = str(int(time.time()))

    info_url = "https://appapi.xiaokaxiu.com/api/v1/web/share/video/" + video_id + "?time=" + timestamp

    temp = "S14OnTD#Qvdv3L=3vm" + "&time=" + timestamp
    x_sign = md5(temp.encode("utf-8")).hexdigest()
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "x-sign": x_sign,
    }
    rep = requests.get(info_url, headers=headers)
    if rep.status_code == 200 and rep.json()["code"] == 0:
        video_info = rep.json()["data"]
        title = video_info["video"]["title"]
        video_url = video_info["video"]["url"][0]
        data["title"] = title
        data["videos"] = [video_url]
        return data
    return {"msg": "获取失败"}


if __name__ == "__main__":
    url = "https://mobile.xiaokaxiu.com/video?id=6552158363189252096"
    print(get(url))
