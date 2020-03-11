import json
import re

import requests


def get(url: str) -> dict:
    """
    videos
    """
    data = {}
    headers = {
        "Host": "share.ippzone.com",
        "Connection": "keep-alive",
        "Content-Length": "45",
        "Origin": "http://share.ippzone.com",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
        "Content-Type": "text/plain;charset=UTF-8",
        "Accept": "*/*",
        "Referer": "http://share.ippzone.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    post_url = "http://share.ippzone.com/ppapi/share/fetch_content"

    pid = re.findall(r"/(\d{1,})", url)
    if not pid:
        data["msg"] = "链接无效，无法获取有效数据"
        return data
    else:
        pid = int(pid[0])

    post_data = {
        "pid": pid,
        "type": "post",
    }

    with requests.post(post_url, headers=headers, data=json.dumps(post_data), timeout=10) as rep:
        if rep.status_code == 200 and rep.json().get("ret") == 1:
            id = rep.json().get("data").get("post").get("imgs")[0].get("id")
            play_url = rep.json().get('data').get('post').get('videos').get(str(id)).get('url')
            data["videos"] = [play_url]
        else:
            data["msg"] = "资源获取失败，请确认输入是否正确"

        return data


if __name__ == "__main__":
    print(get(input("url: ")))