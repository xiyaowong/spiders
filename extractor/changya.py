import re

import requests


def get(url: str) -> dict:
    """
    author、audioName、audios
    """
    data = {"msg": ""}
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    }
    audio_url_pattern = r'<audio src="(http://cdn.singroom.i52hz.com/.*?)" preload="metadata"'
    author_pattern = r'"nickname":"(.*?)",'
    audio_name_pattern = r'"songName":"(.*?)",'

    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            html = rep.text
            author = re.findall(author_pattern, html)
            if author:
                author = author[0]
                data["author"] = author
            audio_name = re.findall(audio_name_pattern, html)
            if audio_name:
                audio_name = audio_name[0]
                data["audioName"] = audio_name
            audio_url = re.findall(audio_url_pattern, html)
            if audio_url:
                audio_url = audio_url[0]
                data["audios"] = [audio_url]
        else:
            data["msg"] = "访问链接内容失败"

        return data


if __name__ == "__main__":
    data = get(input("url: "))
    print(data)
