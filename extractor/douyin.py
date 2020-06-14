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
    api = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_id}&dytk={dytk}"

    # get html text
    rep = requests.get(share_url, headers=headers, timeout=10)
    if not rep.ok:
        return {"msg": "获取失败"}
    html_text = rep.text

    # get item_id, dytk
    item_id = re.findall(r'itemId: "(\d+)"', html_text)
    dytk = re.findall(r'dytk: "(.*?)"', html_text)
    if not item_id or not dytk:
        return {"msg": "获取失败"}
    item_id = item_id[0]
    dytk = dytk[0]

    # get video info
    rep = requests.get(api.format(item_id=item_id, dytk=dytk), headers=headers, timeout=6)
    if not rep.ok or not rep.json()["status_code"] == 0:
        return {"msg": "获取失败"}
    info = rep.json()["item_list"][0]

    data["author"] = info["author"]["nickname"]
    data["title"] = data["videoName"] = info["desc"]
    if info.get('music'):
        data["audioName"] = info["music"]["title"]
        data["audios"] = [info["music"]["play_url"]["uri"]]
    # data["imgs"] = [info["video"]["origin_cover"]["url_list"][0]]

    # get playwm_url -> play_url
    play_url = info["video"]["play_addr"]["url_list"][0].replace('playwm', 'play')

    rep = requests.get(play_url, headers=headers, allow_redirects=False, timeout=6)
    video_url = rep.headers.get('location', '')
    data["videos"] = [video_url]

    return data


if __name__ == "__main__":
    data = get(input('share url: '))
    print(data)
