# from urllib.parse import urlparse
import re

import requests


def get(url: str) -> dict:
    """
    author、audioName、audios
    """
    data = {}
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"}
    info_url = "https://m.lizhi.fm/vodapi/voice/info/{id}"

    # path = urlparse(url).path
    # voiceId = path.split("/")[-1]
    voiceId = re.findall(r"/(\d{1,})", url)
    if not voiceId:
        data["msg"] = "链接无效，解析未成功"
        return data
    else:
        voiceId = voiceId[-1]

    with requests.get(info_url.format(id=voiceId), headers=headers, timeout=10) as rep:
        if rep.status_code == 200 and rep.json().get("code") == 0:
            info = rep.json()
            userName = info.get("data").get("userVoice").get("userInfo").get("name")
            voiceName = info.get("data").get("userVoice").get("voiceInfo").get("name")
            voiceUrl= info.get("data").get("userVoice").get("voicePlayProperty").get("trackUrl")
            data["author"] = userName
            data["audioName"] = voiceName
            data["audios"] = [voiceUrl]
        else:
            data["msg"] = "未能解析成功"

    return data




if __name__ == "__main__":
    url = input("url: ")
    print(get(url))