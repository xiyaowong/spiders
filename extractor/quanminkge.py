import re

import requests


def get(url:str) -> dict:
    '''
    author、audioName、audios、videos
    '''
    data = {"msg":""}
    headers = {
        "accept":
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding":
        "gzip, deflate, br",
        "accept-language":
        "zh-CN,zh;q=0.9",
        "cache-control":
        "max-age=0",
        "sec-fetch-mode":
        "navigate",
        "sec-fetch-site":
        "none",
        "upgrade-insecure-requests":
        "1",
        "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
    }
    singer_pattern = r',"nick":"(.*?)",'
    song_name_pattern = r'"song_name":"(.*?)",'
    audio_pattern = r'"playurl":"(.*?)",'
    video_pattern = r',"playurl_video":"(.*?)",'

    with requests.get(url=url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            html = rep.text
            singer = re.findall(singer_pattern, html)
            song_name = re.findall(song_name_pattern, html)
            audio_url = re.findall(audio_pattern, html)
            video_url = re.findall(video_pattern, html)
            if singer: data["author"] = singer[0]
            if song_name: data["audioName"] = song_name[0]
            if audio_url: data["audios"] = [url for url in audio_url if url != ""]
            if video_url: data["videos"] = [url for url in video_url if url != ""]
        else:
            data["msg"] = "获取失败"

        return data


if __name__ == "__main__":
    data = get(input("url: "))
    print(data)