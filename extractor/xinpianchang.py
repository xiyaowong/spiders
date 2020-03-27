import re

import requests


def get(url: str) -> dict:
    """
    title、imgs、videos(画质不同)
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    session = requests.Session()
    rep = session.get(url, headers=headers, timeout=10)
    if rep.status_code != 200:
        return {"msg": "获取失败"}
    try:
        vid = re.findall(r'vid: "(.*?)",', rep.text)[0]
    except IndexError:
        return {"msg": "获取失败"}

    video_info_url = "http://openapi-vtom.vmovier.com/v3/video/{vid}?expand=resource".format(
        vid=vid)
    rep = session.get(video_info_url, headers=headers, timeout=10)
    if rep.status_code != 200 or rep.json()["status"] != 0:
        return {"msg": "获取失败"}

    video_data = rep.json()["data"]

    title = video_data["video"]["title"]
    cover = video_data["video"]["cover"]
    video_list = video_data["resource"]["progressive"]  # type: list

    videos = []
    for item in video_list:
        videos.append(item.get("https_url") or item.get("url"))

    data["title"] = title
    data["imgs"] = [cover]
    data["videos"] = videos

    return data


if __name__ == "__main__":
    # url = "https://www.xinpianchang.com/a10628284"
    url = input("url: ")
    print(get(url))
