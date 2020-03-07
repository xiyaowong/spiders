import json
from urllib.parse import urlparse

import requests


def get(url: str) -> dict:
    """
    text、audios
    """
    data = {"msg":""}
    headers = {
        "Connection": "keep-alive",
        "Content-Length": "209",
        "Content-Type": "text/plain;charset=UTF-8",
        "Host": "share.izuiyou.com",
        "Origin": "https://share.izuiyou.com",
        "Referer": url,
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    post_url = "https://share.izuiyou.com/api/review/share_review"

    path = urlparse(url).path
    temp = path.split("/")
    pid = temp[-2]
    rid = temp[-1]

    payload = {
        "h_av": "3.0",
        "h_dt": 9,
        "h_nt": 9,
        "h_ch": "web_app",
        "ua":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "pid": f"{pid}",
        "rid": f"{rid}"
    }
    play_host = "http://tbvideo.ixiaochuan.cn/"
    with requests.post(post_url, data=json.dumps(payload), headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            try:
                audio_info = rep.json().get("data").get("review").get("audio")
                voice_text = audio_info.get("voice_text")
                # uri = audio_info.get("uri")
                org_uri = audio_info.get("org_uri")
                data["text"] = voice_text
                data["audios"] = [play_host + org_uri]
            except (TypeError, AttributeError):
                data["msg"] = "获取失败"
        else:
            data["msg"] = "获取失败"

    return data



if __name__ == "__main__":
    print(get(input("url: ")))