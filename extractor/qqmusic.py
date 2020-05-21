import re
import json

import requests


def get(url: str):
    """
    author、audioName、audios
    """
    data = {}
    ios_headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1",
        "referer": "http://y.qq.com"
    }

    # find: songid、songmid and author、audioName
    with requests.get(url, headers=ios_headers, timeout=10) as rep:
        if rep.status_code != 200:
            return {"msg": "链接无效"}
        html = rep.text
        songid = re.findall(r'songid":(\d+),', html)
        songmid = re.findall(r'"songmid":"(.*?)",', html)
        if not (songid or songmid):
            return {"msg": "提取重要信息失败"}
        songid = songid[0]
        songmid = songmid[0]
        data["audioName"] = re.findall(r'"songname":"(.*?)"', html)[0]
        data["author"] = re.findall(r'"name":"(.*?)",', html)[0]

    # vkey
    vkey_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
    params = {
        'data': json.dumps({"req": {"module": "CDN.SrfCdnDispatchServer", "method": "GetCdnDispatch", "param": {"guid": "3982823384", "calltype": 0, "userip": ""}}, "req_0": {"module": "vkey.GetVkeyServer", "method": "CgiGetVkey", "param": {"guid": "3982823384", "songmid": [songmid], "songtype": [0], "uin": "0", "loginflag": 1, "platform": "20"}}, "comm": {"uin": 0, "format": "json", "ct": 24, "cv": 0}})
    }
    with requests.get(vkey_url, params=params, headers=ios_headers, timeout=10) as rep:
        if rep.json()["code"] != 0 and rep.json()['req_0']['code'] != 0:
            return {"msg": "提取重要信息失败"}
        data["audios"] = [
            "https://isure.stream.qqmusic.qq.com/{}".format(rep.json()['req_0']['data']['midurlinfo'][0]['purl'])
        ]

    return data


if __name__ == "__main__":
    # print(get(input("url: ")))
    url = 'https://y.qq.com/n/yqq/song/003tdyG9003JqW.html'
    print(get(url))


# "A000", "ape", 800
# "F000", "flac", 800
# "M800", "mp3", 320
# "C400", "m4a", 128
# "M500", "mp3", 128
