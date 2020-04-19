import re

import requests

headers = {
    'Referer': 'https://m.music.migu.cn/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Mobile Safari/537.36'
}
detail_url = 'http://m.music.migu.cn/migu/remoting/cms_detail_tag?cpid={copyrightId}'
player_url = 'https://app.pd.nf.migu.cn/MIGUM3.0/v1.0/content/sub/listenSong.do?channel=mx&copyrightId={copyrightId}&contentId={contentId}&toneFlag={toneFlag}&resourceType={resourceType}&userId=15548614588710179085069&netType=00'


def get(url: str):
    """http://music.migu.cn/v3/music/song/*********

    author、audioName、audios
    """
    data = {}
    # get copyrightId
    copyrightId = re.findall(r"song/(\d+)", url)[0]

    # get detail
    rep = requests.get(detail_url.format(copyrightId=copyrightId), headers=headers, timeout=6)
    if rep.status_code != 200 or rep.json()["data"] is None:
        return {"msg": "获取失败,请检查链接是否正确"}
    json = rep.json()["data"]  # type: dict

    # author
    singerName = json["singerName"]  # type: list
    author = "&".join(singerName) if len(singerName) > 1 else singerName[0]

    # audioName
    audioName = json["songName"]

    # contentId
    c_item = json.get("qq")  # type:dict

    if not c_item:
        return {"msg": "获取失败"}
    contentId = c_item["productId"]

    # toneFlag
    toneFlag = "HQ" if json["hasHQqq"] == "1" else "LQ"

    video_url = player_url.format(copyrightId=copyrightId,
                                  contentId=contentId,
                                  toneFlag=toneFlag,
                                  resourceType=2)

    data["author"] = author
    data["audioName"] = audioName
    data["videos"] = [video_url]

    return data


if __name__ == "__main__":
    url = "http://music.migu.cn/v3/music/song/69910422841"
    print(get(url))
