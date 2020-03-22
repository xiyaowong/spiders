import requests


def get(url: str):
    """
    author、title、imgs、videos
    """
    data = {}
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like\
            Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    detail_url = url.replace("video/?", "bbq/app-bbq/sv/detail?sv")
    with requests.get(detail_url, headers=headers, timeout=10) as rep:

        if rep.status_code != 200:
            return {"msg": "error occurred!"}

        json = rep.json()
        if json["code"] != 0:
            return {"msg": "error occurred!"}

        author = json["data"]["user_info"]["uname"]
        title = json["data"]["title"]
        imgs = [json["data"]["cover_url"]]
        videos = [json["data"]["play"]["url"]]

        data["author"] = author
        data["title"] = title
        data["imgs"] = imgs
        data["videos"] = videos
    return data


if __name__ == "__main__":
    url = input("url: ")
    print(get(url))
