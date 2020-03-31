# https://www.ted.com/talks/*
import re

import requests


def get(url: str) -> dict:
    """
    title、videoName、videos
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    rep = requests.get(url, headers=headers, timeout=10)
    if rep.status_code == 200:
        text = rep.text
        try:
            title = re.findall(r'<meta name="title" content="(.*?)" />', text)[0]
            mp4 = re.findall(r'"(https://download\.ted\.com.*?mp4\?apikey=.*?)"', text)[-1]
            data["title"] = data["videoName"] = title
            data["videos"] = [mp4]
        except IndexError as e:
            data["msg"] = "获取失败：" + e
    else:
        data["msg"] = "获取失败"

    return data


if __name__ == "__main__":
    url = "https://www.ted.com/talks/bill_gates_how_we_must_respond_to_the_coronavirus_pandemic"
    print(get(url))
