"""
全民搞笑 https://longxia.music.xiaomi.com/share/video/******
"""
import re

import requests


def get(url: str) -> dict:
    """
    title、videoName、videos
    """
    data = {}
    vid = re.findall(r'video/(\d+)', url)
    if vid:
        api = 'https://longxia.music.xiaomi.com/api/share?contentType=video&contentId={}'.format(vid[0])
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        rep = requests.get(api, headers=headers, timeout=5)
        if rep.status_code == 200 and rep.json()['code'] == 200:
            info = rep.json()['data']['videoInfo']['videoInfo']
            data['title'] = data['videoName'] = info['desc']
            data['videos'] = [info['url']]
            return data
    return {'msg': 'failed'}


if __name__ == "__main__":
    print(get('https://longxia.music.xiaomi.com/share/video/6624743459453734912?sharerUserId'))
