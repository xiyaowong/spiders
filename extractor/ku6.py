import re

import requests


# https://m.ku6.com/video/detail?id=*.


def get(url: str):
    """
    title、videos
    """
    data = {}
    rep = requests.get(url, timeout=10)
    try:
        data["title"] = re.findall(r'video-title\'\).text\("(.*?)"\)', rep.text)[0]
        data["videos"] = re.findall(r'{type: "video/mp4", src: "(.*?)"}', rep.text)
    except IndexError as e:
        data["msg"] = f"获取失败{e}"

    return data


if __name__ == "__main__":
    from pprint import pprint
    pprint(get(input("url: ")))
