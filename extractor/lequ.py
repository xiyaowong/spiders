import re

import requests

requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member


def get(url: str) -> dict:
    """
    author、audioName、imgs、audios
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    rep = requests.get(url, headers=headers, timeout=10, verify=False)
    if rep.status_code == 200:
        html = rep.text
        try:
            author = re.findall(r'class="singer_name">(.*?)<', html)[0]
            audioName = re.findall(r'class="song_name">(.*?)<', html)[0]
            imgs = re.findall(r'background-image: url\("(.*?)"\);', html)
            audios = re.findall(r'<audio.*src="(.*?)"  loop="loop"></audio>', html)
            data["author"] = author
            data["audioName"] = audioName
            data["imgs"] = imgs
            data["audios"] = audios
        except Exception:
            data["msg"] = {"msg": "获取失败"}

    return data


if __name__ == "__main__":
    url = "https://api.bestdjb.com/promote/song-share/6477f04370cc22e7d9c2d3ac4265a92a?app_version=1.4.3"
    print(get(url))
