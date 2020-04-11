import re

import requests


def get(url: str) -> dict:
    """
    title、imgs
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    rep = requests.get(url, headers=headers, timeout=6)
    if rep.status_code == 200:
        title = re.findall(r'<meta name="description" content="(.*?)" >', rep.text)
        if title:
            data["title"] = title[0]
        data["imgs"] = re.findall(r'photo-image" src="(.*?)"', rep.text)
    else:
        data["msg"] = "获取失败"
    return data


if __name__ == "__main__":
    from pprint import pprint
    pprint(get(input("url: ")))
