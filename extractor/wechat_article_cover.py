import re

import requests


def get(url: str) -> dict:
    """
    imgs、text
    """
    data = {}
    headers = {
        "user-agent":
        "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/ 53\
        6.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code != 200:
            return {"msg": "错误"}
        img = re.findall(r'<meta property="og:image" content="(.*?)" />', rep.text)
        if img:
            data["imgs"] = [img[0]]
        text = re.findall(r'<meta property="og:title" content="(.*?)" />', rep.text)
        if text:
            data["text"] = text[0]
    return data


if __name__ == "__main__":

    url = input("url: ")
    print(get(url))
