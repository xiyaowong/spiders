import re

import requests


def get(url: str) -> dict:
    """
    """
    data = {}
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",}
    video_info_url = "https://lens.zhihu.com/api/v4/videos/{id}"

    videos = []

    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            ids = re.findall(r'www.zhihu.com/video/(\d{1,})', rep.text)
            ids = list(set(ids)) # 去掉重复元素
        else:
            data["msg"] = "视频获取失败，可能是这个页面没有视频"
            return data

    if not ids:
        data["msg"] = "视频获取失败，可能是这个页面没有视频"
        return data

    for id in ids:
        rep = requests.get(video_info_url.format(id=id), headers=headers, timeout=10)
        if rep.status_code == 200:
            playlist = rep.json().get("playlist")
            temp = playlist.get("HD") or playlist.get("SD") or playlist.get("LD")
            if temp:
                url = temp.get("play_url")
                videos.append(url)
    data["videos"] = [video for video in videos if video != ""]
    return data



if __name__ == "__main__":
    url = input("url: ")
    print(get(url))