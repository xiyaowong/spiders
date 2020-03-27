import re

import requests


def get(url: str) -> dict:
    """
    videos
    """
    data = {}
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    }
    rep = requests.get(url, headers=headers, timeout=10)
    if rep.status_code == 200:
        data["videos"] = re.findall(r'data-video="(.*?)"', rep.text)
    else:
        data["msg"] = "获取失败"

    return data


if __name__ == "__main__":
    # url = "https://tieba.baidu.com/p/6098286801?share=9105&fr=share&sfc=copy&client_type=2&client_version=11.3.8.2&st=1585294971&unique=190E4CEC3908756B412C7ABAE54C772F&red_tag=2618234446"
    url = input("url: ")
    print(get(url))
