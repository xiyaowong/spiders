import re

import requests


def get(url: str) -> dict:
    """
    title、videoName、videos
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    re_title = r'<div class="SharePostCard__content"><span.*?</span>(.*?)</div>'
    re_video = r'<video src="(.*?)".*?></video>'

    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            title = re.findall(re_title, rep.text)
            video = re.findall(re_video, rep.text)
            if title:
                data["title"] = data["videoName"] = title[0]
            if video:
                data["videos"] = video
        else:
            data["msg"] = "失败"

    return data


if __name__ == "__main__":
    url = "https://share.izuiyou.com/detail/147486886?zy_to=applink&to=applink"
    print(get(url))
