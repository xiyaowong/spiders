import re

import requests


def get(url: str):
    """
    title、imgs、videos
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    api = "https://m.immomo.com/inc/microvideo/share/profiles"

    ar = re.findall(r'/(ar.*?)\.html', url)
    if not ar:
        return {"msg": "失败"}
    ar = ar[0]

    payload = {
        "feedids": ar,
        "name": "",
        "avatar": "",
    }

    rep = requests.post(api, data=payload, headers=headers, timeout=6)
    if rep.status_code == 200 and rep.json()["ec"] == 200:
        info = rep.json()["data"]
        title = info["list"][0]["content"]
        img = info["list"][0]["video"]["cover"]["l"]
        video = info["list"][0]["video"]["video_url"]

        data["title"] = data["videoName"] = title
        data["imgs"] = [img]
        data["videos"] = [video]
    else:
        data["msg"] = "失败"

    return data


if __name__ == "__main__":
    from pprint import pprint
    url = "https://m.immomo.com/s/moment/new-share-v2/ar8422649104.html"
    pprint(get(url))
