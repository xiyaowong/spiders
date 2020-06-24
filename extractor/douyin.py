import re

import requests


def get(share_url) -> dict:
    """
    author, title, audioName, audios, videoName, videos
    """
    data = {}
    headers = {
        'accept': 'application/json',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
    }
    api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_id}"

    rep = requests.get(share_url, headers=headers, timeout=10)
    if rep.ok:
        # item_id
        item_id = re.findall(r'video/(\d+)', rep.url)
        if item_id:
            item_id = item_id[0]
            # video info
            rep = requests.get(api.format(item_id=item_id), headers=headers, timeout=10)
            if rep.ok and rep.json()["status_code"] == 0:
                info = rep.json()["item_list"][0]

                data["author"] = info["author"]["nickname"]
                data["title"] = data["videoName"] = info["desc"]
                if info.get('music'):
                    data["audioName"] = info["music"]["title"]
                    data["audios"] = [info["music"]["play_url"]["uri"]]
                # data["imgs"] = [info["video"]["origin_cover"]["url_list"][0]]

                # playwm_url -> play_url
                play_url = info["video"]["play_addr"]["url_list"][0].replace('playwm', 'play')
                data["videos"] = [play_url]
                return data
    return {'msg': '获取失败'}


if __name__ == "__main__":
    data = get(input('share url: '))
    print(data)
