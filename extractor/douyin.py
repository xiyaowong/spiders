import re

import requests


def get(share_url) -> dict:
    """
    title、videos
    """
    data = {}
    headers = {
        'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':
        'gzip, deflate, br',
        'accept-language':
        'zh-CN,zh;q=0.9',
        'cache-control':
        'max-age=0',
        'upgrade-insecure-requests':
        '1',
        'user-agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }

    title_pattern = r'<div class="user-title">(.*?)</div>'
    playwm_url_pattern = r'<video id="theVideo" class="video-player" src="(.*?)" preload'

    with requests.get(share_url, headers=headers, timeout=10) as rep:
        share_url = rep.headers.get('location', share_url)

    with requests.get(share_url, headers=headers, timeout=10) as rep:
        html_text = rep.text

    title = re.findall(title_pattern, html_text)
    if title:
        title = title[0]
        data["title"] = title

    playwm_url = re.findall(playwm_url_pattern, html_text)
    if playwm_url:
        play_url = playwm_url[0].replace('playwm', 'play')
    else:
        data["msg"] = "视频地址获取失败"
        return data

    with requests.get(play_url, headers=headers, allow_redirects=False, timeout=10) as rep:
        video_url = rep.headers.get('location', '')
        data["videos"] = [video_url]

    return data


if __name__ == "__main__":
    data = get(input('share url: '))
    print(data)
