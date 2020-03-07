import re
import requests


def get(url: str) -> dict:
    """
    imgs、videos
    """
    data = {"msg": ""}
    headers = {
        "user-agent":
        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        "Referer": "https://m.bilibili.com/",
    }

    av_number_pattern = r'av([0-9]*)'
    cover_pattern = r'<meta property="og:image" content="(http.*?)"/>'
    video_pattern = r"video_url: '(.*?)',"

    av = re.findall(av_number_pattern, url)
    if av:
        av = av[0]
    else:
        data["msg"] = "链接可能不正确，因为我无法匹配到av号"
        return data

    url = f"https://www.bilibili.com/video/av{av}"

    with requests.get(url, headers=headers, timeout=10) as rep:
        if rep.status_code == 200:
            cover_url = re.findall(cover_pattern, rep.text)
            if cover_url:
                cover_url = cover_url[0]
                if '@' in cover_url:
                    cover_url = cover_url[:cover_url.index('@')]
                data["imgs"] = [cover_url]

            video_url = re.findall(video_pattern, rep.text)
            if video_url:
                video_url = video_url[0]
                data["videos"] = [video_url]
        else:
            data["msg"] = "获取失败"
        return data


if __name__ == "__main__":
    print(get(input("url: ")))
