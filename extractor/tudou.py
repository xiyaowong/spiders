import re
import time

import requests


def get(url: str) -> dict:
    """
    :param url: 视频链接，免费电视剧单集

    :return title: 视频名
    :return videoName: 同title
    :return videos: 视频链接，多个片段。最后一个是视频流地址(m3u8)
    """
    data = {}
    headers_html = {
        "referer": url,
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    headers_info = {
        "referer": url,
        "accept": "application/json",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    host = "https://ups.youku.com/ups/get.json"

    rep = requests.get(url, headers=headers_html, timeout=10)
    if rep.status_code != 200:
        return {"msg": "访问链接失败"}
    vid = re.findall(r'"vid":"(\d+)"', rep.text)
    if not vid:
        return {"msg": "获取视频id失败"}
    vid = vid[0]

    params = {
        #  调试了半天，才发现ckey可以通用，但是暂时不知道过期时间
        "ckey": "122#wppJ/JoGEExRyDpZy4pjEJponDJE7SNEEP7ZpJRBuDPpJFQLpCGwoHZDpJEL7SwBEyGZpJLlu4Ep+FQLpoGUEELWn4yE7SNEEP7ZpERBuDPE+BQPpC76EJponDJLKMQEImb2XDnTtByWAfaPwr8S14Rqur0Nj1sih8TwWMzZF+NtTPnZULbEnh9G8WlODWp1uOjeDLVr8PG6+4EEyFfDqM3bDEpxngR4ul5EDOgPm4AiJDbEfC3mqM3WE8pangL4ul0EDLVr8CpU+4EEyFfDqMfbDEpxnSp4uOIEELXZ8oL6JwTEyF3F7S32EJpadSxwuAuRiRFmYFRiZDPACVgIudh3VaGrVnUkqUbD72siAEVR1Qr4OWZjlGSrnzPs2rh4OY+Z6EbOEBJ8OnDsYwNsTdEhishHohd6L2J+K8z7LZpSitQjj8hrDOAV/ttFwMbpN7KrcdwvCJ7TbxjR5Q0rJaMPlfUv9IYPLIY9KNNy24RBro4psistlkgxw4vO3WXa4M00NlsAH1XADAp8l3+COupmS7LbhxHS2BKVRDZkDyD+xnYIaRahNuJDv7pLt830IQHgDvnq1gJBE75mVDgemdAGyc4ruFk4++Ar9T6gZbfiuacVvtDgzBcEo0r6bi+rvYQuaMy=",
        "utid": "otL9FkVfwnwCASv6yQTaubZ5",  # expires at: 2030-03-25T07:32:14.712Z
        "vid": vid,
        "client_ts": int(time.time()),
        "ccode": "050F",
        "client_ip": "192.168.1.1",
    }
    rep = requests.get(host, params=params, headers=headers_info, timeout=10)
    if rep.status_code != 200 or "error" in rep.json()["data"]:
        return {"msg": "获取视频信息失败"}
    info = rep.json()["data"]
    title = info["video"]["title"]
    stream = info["stream"]  # type: list
    # 取最高画质
    best_steam = sorted(stream, key=lambda item: item["width"])[-1]
    videos = [url_item["cdn_url"] for url_item in best_steam["segs"]]
    m3u8_url = best_steam["m3u8_url"]
    videos.append(m3u8_url)

    data["title"] = data["videoName"] = title
    data["videos"] = videos

    return data


if __name__ == "__main__":
    from pprint import pprint
    pprint(get(input("url: ")))
