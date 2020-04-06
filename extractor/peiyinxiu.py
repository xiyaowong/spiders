import re

import requests


def get(url: str) -> dict:
    """
    title、videos
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    rep = requests.get(url, headers=headers, timeout=10)
    if rep.status_code != 200:
        return {"msg": "获取失败"}
    html = rep.text
    data["title"] = re.findall(r'data-title="(.*?)"', html)[0]
    data["videos"] = re.findall(r"\sfilmurl: '(.*?)',", html)
    return data


if __name__ == "__main__":
    url = "http://peiyinxiu.com/m/127066455"
    print(get(url))
