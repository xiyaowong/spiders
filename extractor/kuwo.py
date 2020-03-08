# 320 192 128
import re

import requests


def get(url: str) -> dict:
    """
    author、audioName、audios
    """
    data = {"msg": ""}
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.kuwo.cn",
        "Referer": "http://www.kuwo.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    }
    song_info_url_format = "http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId={id}"
    mp3_url_format = "http://www.kuwo.cn/url?format=mp3&rid={id}&response=url&type=convert_url3&br={quality}&from=web"

    # http://www.kuwo.cn/play_detail/*********
    id = re.findall(r"/(\d{1,})", url)
    if id:
        id = id[0]
    else:
        data["msg"] = "不支持输入的链接形式"
        return data

    session = requests.session()

    # 得到最高品质以及歌曲信息
    with session.get(song_info_url_format.format(id=id), headers=headers, timeout=10) as rep:
        if rep.status_code == 200 and rep.json().get("status") == 200:
            best_quality = rep.json().get("data").get(
                "songinfo").get("coopFormats")[0]
            author = rep.json().get("data").get("songinfo").get("artist")
            song_name = rep.json().get("data").get("songinfo").get("songName")
            pic = rep.json().get("data").get("songinfo").get("pic")
            data["author"] = author
            data["audioName"] = song_name
            data["imgs"] = [url for url in pic if url != ""]
        else:
            data["msg"] = "获取失败"
            return data

    if not best_quality:
        best_quality = "128kmp3"

    # 得到歌曲链接
    with session.get(mp3_url_format.format(id=id, quality=best_quality), headers=headers, timeout=10) as rep:
        if rep.status_code == 200 and rep.json().get("code") == 200:
            play_url = rep.json().get("url", "")
            data["audios"] = [url for url in play_url if url != ""]
        else:
            data["msg"] = "获取音频链接失败"

    return data


if __name__ == "__main__":
    print(get(input("url:  ")))
