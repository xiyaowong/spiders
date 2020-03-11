import re
import json

import requests


def get(url:str) -> dict:
    """
    author、audioName、imgs、audios
    """
    data = {}
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'referer':
        'https://www.kugou.com/song/',
        'cookie':
        'kg_mid=f679eeece44cf6bec74d2867be4901f7; kg_dfid=2kuKRO3GStCZ0VBY9V12pXeT; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1574177549,1576216623,1576386693; kg_mid_temp=f679eeece44cf6bec74d2867be4901f7; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1576387198',
    }
    song_info_url = "https://wwwapi.kugou.com/yy/index.php"

    hash = re.findall(r"hash=([a-zA-Z0-9]+)", url)
    if hash:
        hash = hash[0]
    else:
        hash_pattern = r'"hash":"(.*?)",'
        with requests.get(url, headers=headers, timeout=10) as rep:
            if rep.status_code == 200:
                hash = re.findall(hash_pattern, rep.text)
            if not hash:
                data["msg"] = "关键信息获取失败"
                return data
            hash = hash[0]

    params = {
        "r": "play/getdata",
        "callback": "jQuery191003428174711713661_1583566461495",
        "hash": hash,
        "album_id": 0,
        "dfid": "2kuKRO3GStCZ0VBY9V12pXeT",
        "mid": "f679eeece44cf6bec74d2867be4901f7",
        "platid": 4,
    }

    with requests.get(song_info_url, params=params, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            text = rep.text[rep.text.index("(")+1:].replace(")", "").replace(";", "")
            data_ = json.loads(text)
            if data_.get("err_code") == 0:
                info = data_.get("data")
                author_name = info.get('author_name')
                song_name = info.get('song_name')
                play_url = info.get('play_url')
                img = info.get('img')
                data["author"] = author_name
                data["audioName"] = song_name
                data["audios"] = [play_url]
                data["imgs"] = [img]
            else:
                data["msg"] = "。。。好像失败了"
        else:
            data["msg"] = "。。。好像失败了"

    return data


if __name__ == "__main__":
    print(get(input('url: ')))