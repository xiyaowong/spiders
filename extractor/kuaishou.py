import json
import re

import requests
from lxml import etree


def get(url: str) -> dict:
    """
    title、imgs、videos
    """
    data = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
        "Cookie": "did=web_68e0268146694843a92700d2de49a0a6;"
    }
    # rewrite the desktop url
    temp = re.findall(r'live\.kuaishou\.com/u/\w+/(\w+)', url)
    if temp:
        url = 'https://c.kuaishou.com/fw/photo/{}'.format(temp[0])

    rep = requests.get(url, headers=headers, timeout=10)
    if rep.status_code == 200:
        tree = etree.HTML(rep.text)  # pylint: disable=c-extension-no-member

        # title
        desc = tree.xpath(r"//meta[@name='description']/@content")
        if desc:
            data['title'] = desc[0]

        # imgs
        imgs = tree.xpath(r"//img[@class='play-long-image']/@src")
        if imgs:
            data['imgs'] = ["https:" + i for i in imgs]

        # video
        hide_data = tree.xpath(r"//div[@id='hide-pagedata']/@data-pagedata")
        if hide_data:
            try:
                data_ = json.loads(hide_data[0])
                data['video'] = [data_['video']['srcNoMark']]
                data['title'] = data['videoName'] = data_['video']['caption']
            except Exception:
                pass

        return data

    return {'msg': 'failed...'}


if __name__ == "__main__":
    from pprint import pprint
    pprint(get(input("url: ")))
