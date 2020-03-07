import re

import requests


def get(url: str) -> dict:
    """
    title、videos
    """
    data = {"msg":""}
    headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}

    title_re = r'"title": "(.*?)",'
    mp4_720p_mp4_re = r'"mp4_720p_mp4": "(.*?)",'
    mp4_hd_mp4_re = r'"mp4_hd_mp4": "(.*?)",'
    mp4_ld_mp4_re = r'"mp4_ld_mp4": "(.*?)"'

    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            text = rep.text
            title = re.findall(title_re, text)
            mp4_720p_mp4 = re.findall(mp4_720p_mp4_re, text)
            mp4_hd_mp4 = re.findall(mp4_hd_mp4_re, text)
            mp4_ld_mp4 = re.findall(mp4_ld_mp4_re, text)
            if title:
                data["title"] = title[0]
            data["videos"] = mp4_720p_mp4 or mp4_hd_mp4 or mp4_ld_mp4
        else:
            data["msg"] = "获取失败"

        return data


if __name__ == "__main__":
    url = input('url: ')
    print(get(url))