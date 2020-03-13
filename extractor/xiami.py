# author: wongxy
# --------------
# https://www.xiami.com/api/song/getPlayInfo?_q=%7B%22songIds%22:[1810488394]%7D&_s=02a18c2bf56edd99c87bf5a7231e6f82
import re
from urllib.parse import urlparse
from hashlib import md5

import requests

# TODO:


class XiaMi(object):

    def __init__(self):
        self.data = {}
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh,zh-CN;q=0.9,en;q=0.8",
            "cookie": "xmgid=6f3a263a-fb8e-43d4-9119-905b5588a958; cna=ASNzFDoKD38CAXcnfiWoB4Jz; gid=158389354845327; _xiamitoken=c1b1b4777110d1c0fc1514e67ff52cff; _unsign_token=db9b5e5c788bf9e652e9a78150b7da22; xm_sg_tk=32f89397718bf5970131eab1823d3edf_1584105835953; xm_sg_tk.sig=Vy9InSd5lMdvhTl4t7k-zAYRZQAxETyLApZuVL1qmC4; _xm_umtoken=T76545341E45A911C2A71A21E0A12D9FAA506F4545587D2301ECAE8FF93; _xm_cf_=pc-zl23kcdLeBwsfmTmAyAOO; xm_oauth_state=7ee6e4be34a6ff21a1d5e4536069f7ac; isg=BD090LfGPzdzTpjEmWosJ_uPTJk32nEshP6div-JyheKNk5owyrJ_K6n4GJwtonk; l=dBNBtMNgqdPg8za-BOfNicRxWJ_92Ldj1sPr_y1L0ICPOrW5AYJlWZqMoytXCnGNnssw5354uljQBa29qyCSnxv9-pmE9G9tDLTh.",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
        }
        self.win_headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh,zh-CN;q=0.9,en;q=0.8",
            "cookie": "xmgid=6f3a263a-fb8e-43d4-9119-905b5588a958; cna=ASNzFDoKD38CAXcnfiWoB4Jz; gid=158389354845327; _xiamitoken=c1b1b4777110d1c0fc1514e67ff52cff; _unsign_token=db9b5e5c788bf9e652e9a78150b7da22; xm_sg_tk=32f89397718bf5970131eab1823d3edf_1584105835953; xm_sg_tk.sig=Vy9InSd5lMdvhTl4t7k-zAYRZQAxETyLApZuVL1qmC4; _xm_umtoken=T76545341E45A911C2A71A21E0A12D9FAA506F4545587D2301ECAE8FF93; _xm_cf_=pc-zl23kcdLeBwsfmTmAyAOO; xm_oauth_state=7ee6e4be34a6ff21a1d5e4536069f7ac; isg=BD090LfGPzdzTpjEmWosJ_uPTJk32nEshP6div-JyheKNk5owyrJ_K6n4GJwtonk; l=dBNBtMNgqdPg8za-BOfNicRxWJ_92Ldj1sPr_y1L0ICPOrW5AYJlWZqMoytXCnGNnssw5354uljQBa29qyCSnxv9-pmE9G9tDLTh.",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
            "xm-ua": "DIl58SLFxFNndSV1GFNnMQVYkx1PP5tKe1siZu/86PR1u/Wh1Ptd+WOZsHHWxysSfAOhNJpdVWsdVJNsfJ8Sxd8WKVvNfAS8aS8fAOzYARzPyPc3JvtnPHjTdKfESTdnuTW6ZPvk2pNDh4uFzotgdMEFkzQ5wZVXl2Pf1/Y6hLK0OnCNxBj3+nb0v72gZ6b0td+WOZsHHWxysSo/0y9D2K42SaB8Y/+aD2K42SaB8Y/+ahU+WOZsHcrxysooUeND"
        }
        self.session = requests.Session()
        self.play_info_url = "https://www.xiami.com/api/song/getPlayInfo"
        # self.song_info_url = "https://www.xiami.com/api/song/getSongs?_s=7aed46569fa739f4a0f1eeb755713ecd&_xm_cf_=mw_3ESWKH_7eNzrsI2HduD9K"

    def get(self, url: str):
        rep = self.session.get(url, headers=self.headers, timeout=10)
        if rep.status_code != 200:
            return {"msg": "链接无效或不支持"}
        songid = re.findall(
            r'"songId":"(\d+)",', rep.text)
        if not songid:
            return {"msg": "链接无效或不支持"}
        songName = re.findall(
            r'{"songName":"(.*?)",', rep.text
        )
        singer = re.findall(r'{"artistName":"(.*?)",', rep.text)
        if songName:
            self.data["audioName"] = songName[0]
        if singer:
            self.data["author"] = singer[0]
        songid = songid[0]
        print(songid)
        _q = str({"songIds": [songid]})
        _s = self._get_params_s(self.play_info_url, _q)
        if not _s:
            return {"msg": "获取失败"}
        params = {
            "_q": _q,
            "_s": _s
        }
        print(params)
        rep = self.session.get(
            self.play_info_url, params=params, headers=self.win_headers, timeout=10)  # type: list
        print(rep.json())
        try:
            play_infos = rep.json()[
                "result"]["data"]["songPlayInfos"][0]["playinfos"]
            for item in play_infos:
                audio_url = item.get("listenFile")
                if audio_url:
                    break
                self.data["audios"] = audio_url
        except TypeError:
            return {"msg": "获取失败"}
        finally:
            return self.data

    def _get_params_s(self, api_url: str, _q: str) -> str:
        path = urlparse(api_url).path
        xm_sg_tk = self._get_xm_sg_tk()
        if not xm_sg_tk:
            return None
        data = xm_sg_tk + "_xmMain_" + path + "_" + _q
        return md5(bytes(data, encoding="utf-8")).hexdigest()

    def _get_xm_sg_tk(self):
        xm_sg_tk = self.session.cookies.get("xm_sg_tk", None)
        if xm_sg_tk is None:
            return None
        return xm_sg_tk.split("_")[0]


def get(url: str):
    return XiaMi().get(url)


if __name__ == "__main__":
    print(get(input("url: ")))
