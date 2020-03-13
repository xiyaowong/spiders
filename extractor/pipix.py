# author: wongxy
# --------------
# https://h5.pipix.com/item/******************
import re
import requests


def get(url: str) -> dict:
    """
    title、audios
    """
    data = {}
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    item_id = re.findall(r"item/(\d+)", url)
    if not item_id:
        return {"msg": "获取失败"}
    item_id = item_id[0]
    info_url = f"https://h5.pipix.com/bds/webapi/item/detail/?item_id={item_id}&source=share"
    with requests.get(info_url, headers=headers, timeout=10) as rep:
        if rep.status_code != 200 or rep.json().get("status_code") != 0:
            return {"msg": "获取失败"}
        info = rep.json()["data"]["item"]
        data["title"] = info["share"]["title"]
        data["audios"] = [info["origin_video_download"]["url_list"][0]["url"]]



    return data


if __name__ == "__main__":
    print(get(input("url: ")))