import json
import re

import requests


def get(url: str) -> dict:
    """
    title、imgs、videos
    """
    data = {}
    failed = {'msg': 'failed...'}
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
        "Cookie": "did=web_68e0268146694843a92700d2de49a0a6;"
    }
    # rewrite desktop url
    temp = re.findall(r'live\.kuaishou\.com/u/\w+/(\w+)', url)
    if temp:
        url = 'https://c.kuaishou.com/fw/photo/{}'.format(temp[0])

    rep = requests.get(url, headers=headers, timeout=10)
    if rep.status_code != 200:
        return failed

    page_data = re.findall(r'<script type="text/javascript">window\.pageData= (\{.*?\})</script>', rep.text)
    if not page_data:
        return failed

    try:
        page_data = json.loads(page_data[0])
    except Exception:
        print('kuaishou loads json failed')
        return failed

    video_info = page_data['video']
    data['title'] = video_info['caption']
    # 获取视频
    try:  # 如果出错，则可能是长图视频
        data['videos'] = [video_info['srcNoMark']]
    except Exception:
        pass
    else:
        data['videoName'] = data['title']
    # 获取图片
    try:  # 如果出错，则可能是普通视频；
        images = video_info['images']
        imageCDN = video_info['imageCDN']
        # 如果是长图视频，则这几项一定存在
        assert images is not None
        assert imageCDN is not None
    except Exception:
        pass
    else:
        data['imgs'] = [imageCDN + i['path'] for i in images]
    return data


if __name__ == "__main__":
    from pprint import pprint
    pprint(get(input("url: ")))
