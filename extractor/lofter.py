import re

import requests


def get(url: str) -> dict:
    """
    videos
    """
    data = {}
    rep = requests.get(url, timeout=10)
    if rep.status_code == 200:
        data["videos"] = re.findall(r'<video.*?src="(.*?)"', rep.text)
    else:
        data["msg"] = "获取失败"

    return data


if __name__ == "__main__":
    # url = "https://yan5236.lofter.com/post/1d6ced3e_1c74f6df6"
    url = input("url: ")
    print(get(url))
