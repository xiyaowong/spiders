import re

import requests


def get(url: str) -> dict:
    """
    title、videos
    """
    data = {}
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    info_url = "https://api-new.acfunchina.com/rest/app/play/playInfo/mp4?videoId={}&resourceId={}&resourceType=2&mkey=AAHewK3eIAAyMjAzNTI2NDMAAhAAMEP1uwS3Vi7NYAAAAJumF4MyTTFh5HGoyjW6ZpdjKymALUy9jZbsMTBVx-F10EhxyvpMtGQbBCYipvkMShM3iMNwbMd9DM6r2rnOYRVEdr6MaJS4yxxlA_Sl3JNWup57qBCQzOSC7SZnbEsHTQ%3D%3D&market=xiaomi&product=ACFUN_APP&sys_version=10&app_version=6.20.0.915&boardPlatform=sdm845&sys_name=android&socName=UNKNOWN&appMode=0"
    # info_url = "https://m.acfun.cn/rest/mobile-direct/play/playInfo/singleQuality?videoId={}&resourceId={}&resourceType=2&mkey=AAHewK3eIAAyMjA5NTQ0MDACARAAMEP1uwPvjQhfQAAAAIAq7FtjRH%2Fn9rSMzs1AUNhmIS6eARtddADGgoGewjnABMg39tddqp9dTUq%2Ffd7MBisH5JpVc1bpf64a%2Bz3qrdI%3D"

    # get videoId, resourceIds
    re_title = r'<title>(.*?)</title>'
    re_videoId = r'"vid":"(\d+)",'
    re_resourceId = r'"ac":"(\d+)",'

    try:
        rep_html = requests.get(url, headers=headers, timeout=10)

        title = re.findall(re_title, rep_html.text)[0]
        videoId = re.findall(re_videoId, rep_html.text)[0]
        resourceId = re.findall(re_resourceId, rep_html.text)[0]

        rep_info = requests.get(info_url.format(videoId, resourceId), headers=headers, timeout=10)

        video = rep_info.json()["playInfo"]["streams"][0]["playUrls"][0]
    except (IndexError, TypeError):
        data["msg"] = "获取失败"
    else:
        data["title"] = title
        data["videos"] = [video]

    return data


if __name__ == "__main__":
    url = "https://m.acfun.cn/v/?ac=14134176&part=2"
    print(get(url))
