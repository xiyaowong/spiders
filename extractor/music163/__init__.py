from .music163 import Wangyiyun


def get(url: str) -> dict:
    """
    aduios或者videos
    """
    data = {}
    wangyiyun = Wangyiyun()
    resource_url = wangyiyun.get(url)
    if not resource_url:
        return {"msg": "获取失败"}
    if "mv" in url or "video" in url:
        data["videos"] = [resource_url]
    elif "song" in url:
        data["audios"] = [resource_url]
    return data


__all__ = ["get"]
