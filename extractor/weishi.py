import json
from urllib.parse import urlparse, parse_qs

import requests


data = {"msg": ""}
headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-length": "63",
    "content-type": "application/json",
    "cookie": "pgv_pvi=9657849856; pgv_pvid=2069474799; RK=aHJszqfoXm; ptcz=0fc0035b9509215f060561393c09f6cde3bccc1953e79c2b5b1ec450e4e67f19; LW_uid=s1i5E5d4v2a1p5n702J1O2y0q8; eas_sid=M1k5T5N4O28185X7J291x2K1A3; o_cookie=286183317; pac_uid=1_286183317; ied_qq=o0286183317; LW_sid=x1Y5D6W4h4H516F6X9l9V8S8Z3; tvfe_boss_uuid=fbb4b39b5afeb49b; psrf_qqopenid=A140C50D3D791392EA89131C8B01FE1D; psrf_qqaccess_token=D2F43F3C25900E66193345D276AF9559; psrf_qqrefresh_token=E48409D7E8E4F3D5C3869F104380AB3E; psrf_qqunionid=002C01991CFB436BCD8A27A0EE1DB9FF; qm_keyst=Q_H_L_2ajiOt50eapmue6Eg1-l_W6XztEBr_u0vZJAPs4xctJZNJdsEZONiDnNJ206icA; psrf_musickey_createtime=1574482649; psrf_access_token_expiresAt=1582258649; person_id_bak=5295507715828209; person_id_wsbeacon=5689667751647505; wsreq_logseq=336060008",
    "origin": "https://h5.weishi.qq.com",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1",
    "x-requested-with": "XMLHttpRequest",
}


# 未登录时分享的链接
# url = "https://h5.weishi.qq.com/weishi/wsplay/challenge?feedid=6YV0vjeP71IHTsV08&challegeid=100026&spid=8039370850869145600&qua=v1_and_weishi_6.5.0_588_312027000_d&chid=127081004&pkg=&attach=cp_reserves3_1190370002"
def _get_not_logged(url: str) -> dict:
    global data
    post_url = "https://h5.weishi.qq.com/webapp/json/challenge_feedrank/GetChallengeFeedDetail?t=0.2602280426206063&g_tk="

    query = parse_qs(urlparse(url).query)
    try:
        feedid = query.get('feedid')[0]
        challenge_id = query.get('challegeid')[0]
    except:
        data["msg"] = "获取失败"
        return data

    payload = {
        "feedid": feedid,
        "challenge_id": challenge_id,
        "type": 0,
    }

    with requests.post(post_url, headers=headers, data=json.dumps(payload), timeout=10) as rep:
        if rep.status_code == 200:
            video_info = rep.json().get("data").get('feedinfos')[0]
            title = video_info.get("feed_desc")
            play_url = video_info.get("video_url")
            data["title"] = title
            data["videos"] = [play_url]
        else:
            data["msg"] = "获取失败"

    return data


# 登录后分享的链接
# url = "https://h5.weishi.qq.com/weishi/feed/770BSyaon1IQcqdbr/wsfeed?wxplay=1&id=770BSyaon1IQcqdbr&spid=8039370850869145600&qua=v1_and_weishi_6.5.0_588_312027000_d&chid=100081014&pkg=3670&attach=cp_reserves3_1000370011"
def _get_logged(url: str) -> dict:
    global data
    post_url = "https://h5.weishi.qq.com/webapp/json/weishi/WSH5GetPlayPage?t=0.16820895093158983&g_tk="

    query = parse_qs(urlparse(url).query)
    try:
        feedid = query.get('id')[0]
    except:
        data["msg"] = "获取失败"
        return data

    payload = {
        "feedid": feedid,
        "recommendtype": 0,
        "datalvl": "all",
        "_weishi_mapExt": {}
    }

    with requests.post(post_url, headers=headers, data=json.dumps(payload), timeout=10) as rep:
        if rep.status_code == 200:
            video_info = rep.json().get('data').get('feeds')[0]
            title = video_info.get("feed_desc")
            play_url = video_info.get("video_url")
            data["title"] = title
            data["videos"] = [play_url]
        else:
            data["msg"] = "获取失败"

    return data


def get(url: str) -> dict:
    return _get_not_logged(url) if url.startswith("https://h5.weishi.qq.com/weishi/wsplay/challenge") else _get_logged(url)


if __name__ == "__main__":
    print(get(input("url: ")))
