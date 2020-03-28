import re
import requests


def get(url: str) -> dict:
    """
    title、videos
    """
    data = {}
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    re_title = r'<title>(.*?)</title>'
    re_video = r'<video class="video" src=(.*?)></video>'

    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            title = re.findall(re_title, rep.text)
            video = re.findall(re_video, rep.text)
            if title:
                data["title"] = title
            if video:
                data["videos"] = [video]
        else:
            data["msg"] = "失败"

    return data


if __name__ == "__main__":
    url = "https://haokan.baidu.com/v?vid=10422427972023610990&tab=recommend"
    print(get(url))
