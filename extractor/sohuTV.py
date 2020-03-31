import re

import requests


def get(url: str) -> dict:
    """
    title、videoName、videos
    """
    data = {}
    session = requests.Session()
    ERROR = {"msg": "获取失败"}
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    videoInfo_url = "https://my.tv.sohu.com/play/videonew.do"
    playInfo_url = "https://data.vod.itc.cn/ip"

    with session.get(url, headers=headers, timeout=10) as rep_html:
        if rep_html.status_code != 200:
            return ERROR
        vid = re.findall(r",vid: '(\d+)'", rep_html.text)
        if not vid:
            return ERROR
        vid = vid[0]

    videoInfo_params = {
        "vid": vid,
        "ver": 31,
        "ssl": 1,
        "referer": url
    }
    with session.get(videoInfo_url, params=videoInfo_params, timeout=10) as videoInfo_rep:
        if videoInfo_rep.status_code != 200:
            return ERROR
        videoInfo = videoInfo_rep.json()["data"]
        tvName = videoInfo["tvName"]
        data["title"] = data["videoName"] = tvName

        video_path = videoInfo["su"][0]
        key = videoInfo["hc"][0] if videoInfo.get("hc") else videoInfo["ck"][0]
        if not video_path or not key:
            return ERROR

    playInfo_params = {
        "new": video_path,
        "num": 1,
        "key": key,
    }
    with session.get(playInfo_url, params=playInfo_params, timeout=10) as playInfo_rep:
        if playInfo_rep.status_code != 200:
            return ERROR
        play_url = playInfo_rep.json()["servers"][0]["url"]
        data["videos"] = [play_url]

    return data


if __name__ == "__main__":
    url = input("url: ")
    print(get(url))
