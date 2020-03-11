# qianqian music
# music.taihe.com
import re
import requests


def get(url: str) -> dict:
    """
    url sample: http://music.taihe.com/song/********

    author、audioName、imgs、audios
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    }
    songinfo_format_url = "http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&songid={songid}&from=web"

    songid = re.findall(r"song/(\d+)", url)
    if not songid:
        data["msg"] = "无法获取有效消息"
        return data
    songid = songid[0]
    songinfo_url = songinfo_format_url.format(songid=songid)
    with requests.get(songinfo_url, headers=headers, timeout=10) as rep:
        if rep.status_code != 200:
            data["msg"] = "无法获取有效消息"
            return data
        result = rep.json()
        data["author"] = result["songinfo"]["artist"]
        data["audioName"] = result["songinfo"]["title"]
        data["imgs"] = [result["songinfo"]["album_1000_1000"]]
        data["audios"] = [result["bitrate"]["show_link"] or result["bitrate"]["file_link"]]

    return data


if __name__ == "__main__":
    import pprint
    pprint.pprint(get(input("url: ")))