import json
from urllib.parse import urlparse, parse_qs

import requests

# TODO: 支持小视频

def get(url: str) -> dict:
    """
    author、title、videos
    """
    data = {}
    if "new.3qtt.cn" in url:  # 短连接转长连接
        url = requests.get(url).url

    data_url_format = "http://api.1sapp.com/content/getRecommendV3?key={key}&content_id={content_id}&limit=1"
    play_host = "http://v4.qutoutiao.net/"

    query = urlparse(url).query
    querys = parse_qs(query)
    content_id = querys["content_id"][0]
    key = querys["key"][0]
    data_url = data_url_format.format(content_id=content_id, key=key)

    rep = requests.get(data_url, timeout=10)
    if rep.status_code != 200 or rep.json()["code"] != 0:
        return {"msg": "获取失败"}

    # from pprint import pprint
    # pprint(rep.json())
    json_url = rep.json()["data"]["data"][0]["urlJson"]
    rep = requests.get(json_url, timeout=10)
    if rep.status_code != 200:
        return {"msg": "获取失败"}
    # 整理
    video_data = json.loads(rep.text.replace("cb(", "").replace(")", ""))
    detail = video_data["detail"].replace("\\", "")
    video_data["detail"] = json.loads(detail)

    data["author"] = video_data["nickname"]
    data["title"] = video_data["title"]
    address = video_data["detail"]["address"]

    urls = [add["url"] for add in address]
    for q in ["hd.mp4", "hhd.mp4", "ld.mpp4", "hld.mp4"]:
        for i in urls:
            if q in i:
                data["videos"] = [play_host + i]
                break

    return data


if __name__ == "__main__":
    from pprint import pprint
    pprint(get(input("url: ")))
