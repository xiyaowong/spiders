# author: wongxy
# --------------
# 5sing.kugou.com
import re
import json

import requests


def get(url: str) -> dict:
    """
    author、audioName、audios
    """
    data = {}
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }

    songinfo_format_url = "http://service.5sing.kugou.com/song/getsongurl?&songid={songid}&songtype=fc&from=web&version=6.6.72"

    songid = re.findall(r"/(\d+)", url.replace("5sing", ""))
    if not songid:
        return {"msg": "无法从链接获取关键信息"}
    songid = songid[0]

    songinfo_url = songinfo_format_url.format(songid=songid)
    with requests.get(songinfo_url, headers=headers, timeout=10) as rep:
        if rep.status_code != 200:
            return {"msg": "获取失败, 链接可能无效"}
        json_ = json.loads(rep.text[1: -1])
        if json_["code"] != 0:
            return {"msg": "获取失败, 链接可能无效"}
        info = json_["data"]
        data["author"] = info["user"]["NN"]
        data["audioName"] = info["songName"]
        data["audios"] = [
            info.get("squrl") or info.get("hqurl") or info.get("lqurl")
        ]

    return data


if __name__ == "__main__":
    from pprint import pprint
    pprint(get("http://5sing.kugou.com/fc/15717150.html"))
    # print(get(input("url: ")))
