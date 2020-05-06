import re

import requests


def get(url: str) -> dict:
    """https://www.58pic.com/newpic/*.html

    imgs
    """
    rep = requests.get(url, timeout=6)
    if not rep.ok:
        return {"msg": "失败"}
    pre_url = re.findall(r'<meta property="og:image" content="//(.*?)!.*?"/>', rep.text)
    if not pre_url:
        return {"msg": "失败"}
    pre_url = pre_url[0]  # type: str
    img_url = pre_url.replace("preview.qiantucdn.com", "https://pic.qiantucdn.com")
    return {"imgs": [img_url], "msg": f"下载时需要设置referer: {url}"}


if __name__ == "__main__":
    # url = input("url: ")
    url = "https://www.58pic.com/newpic/34673009.html"
    print(get(url))
