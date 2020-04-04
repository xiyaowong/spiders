import json
from urllib.parse import urlparse

import requests
import re

def get(url: str) -> dict:
    """
    text、videos
    """
    data = {}
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "COMMON_LID=d8d795e732f64cd28cbbce9ee76688af; Hm_lvt_a42a9a9e9ea0c8ce010e90569767e0f4=1585966701; Hm_lpvt_a42a9a9e9ea0c8ce010e90569767e0f4=1585969995",
        "DNT": "1",
        "Host": "quanmin.hao222.com",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    }
    re_video = r'<meta property="og:videosrc" content="(.*?)">'
    re_title = r'<meta property="og:title" content="(.*?)">'

    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            title = re.findall(re_title, rep.text)
            video = re.findall(re_video, rep.text)
            if title:
                data["title"] = title[0]
            if video:
                data["videos"] = video
        else:
            data["msg"] = "失败"
    return data


if __name__ == "__main__":
    url = "https://quanmin.hao222.com/sv2?source=share-h5&pd=qm_share_mvideo&vid=3877781674274744362&shareTime=1585969946&shareid=0746467921&shared_cuid=0ivn8laMv8l9uHuI_PSua_uS2u_Wav8dYu2ku_iCStloiBaR_8S08jf2QP0Hf1uea1FmA&shared_uid=gO2Ri_aIvtelA"
    print(get(url))
