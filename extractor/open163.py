# pylint: disable=W0123
import re
import requests


def get(url: str) -> dict:
    """
    videos
    """
    data = {}
    data["videos"] = []
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    re_url = r'mid:(.*?),.*?mp4SdUrlOrign:(.*?),.*?mp4HdUrlOrign:(.*?),.*?mp4ShdUrlOrign:(.*?),'
    rep = requests.get(url, headers=headers, timeout=10)
    items = re.findall(re_url, rep.text)
    for item in items:
        # 倒序取最高画质
        for video_url in item[::-1]:  # type: str
            # print(url)
            if "http" in video_url:
                video_url = eval(video_url).replace("\\u002F", "/")
                data["videos"].append(video_url)
                break
    return data


if __name__ == "__main__":
    url = "http://open.163.com/newview/movie/free?pid=M8LI1JCE6&mid=M8LI3BQ60"
    print(get(url))
