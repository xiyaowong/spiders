# hdflvUrl="",sdflvUrl="",hdUrl="",sdUrl="",ldUrl="",srcUrl="https://video.pearvideo.com/mp4/adshort/20200328/cont-1665047-11947733-122441_adpkg-ad_hd.mp4",
# data-title="奥运推迟后东京新冠确诊数翻倍，《纽约时报》发文质疑" data-summary="从3月23日起，东京地区的新冠病毒确诊数就连续4天上涨。在24日官宣东京奥运推迟之后，第二天确诊数更是直接翻倍。《纽约时报》写了一篇文章，列出了各种数据，质疑此前东京为了奥运会而牺牲检测。"

import re
import requests


def get(url: str) -> dict:
    """
    title、videos、text
    """
    data = {}
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    }
    try:
        rep = requests.get(url, headers=headers, timeout=10)
        data["title"], data["text"] = re.findall(r'data-title="(.*?)" data-summary="(.*?)"', rep.text)[0]
        data["videos"] = re.findall(r'srcUrl="(.*?\.mp4)",', rep.text)
    except (ConnectionError, IndexError, TypeError):
        data["msg"] = "获取失败"

    return data


if __name__ == "__main__":
    url = "https://www.pearvideo.com/video_1664989"
    print(get(url))
