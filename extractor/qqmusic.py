import re

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


    # vkey_url = "https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg"
    # songinfo_url = f"https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI20753546479271834&g_tk=1780073730&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22songinfo%22%3A%7B%22method%22%3A%22get_song_detail_yqq%22%2C%22param%22%3A%7B%22song_type%22%3A0%2C%22song_mid%22%3A%22{songmid}%22%2C%22song_id%22%3A{songid}%7D%2C%22module%22%3A%22music.pf_song_detail_svr%22%7D%7D"
    vkey_url = f"https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&uin=3989&songmid={songmid}&filename=C400{songmid}.m4a&guid=9234328946"

    # get vkey
    with requests.get(vkey_url, headers=ios_headers, timeout=10) as rep:
        if rep.json()["code"] != 0:
            return {"msg": "提取重要信息失败"}
        filename = rep.json()["data"]["items"][0]["filename"]
        vkey = rep.json()["data"]["items"][0]["vkey"]
        data["audios"] = [f"https://isure.stream.qqmusic.qq.com/{filename}?guid=9234328946&vkey={vkey}&uin=3989&fromtag=66"]

    return data


if __name__ == "__main__":
    print(get(input("url: ")))


# "A000", "ape", 800
# "F000", "flac", 800
# "M800", "mp3", 320
# "C400", "m4a", 128
# "M500", "mp3", 128