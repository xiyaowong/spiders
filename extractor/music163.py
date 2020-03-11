import json
import requests
import base64
import codecs
import os
import re
from Crypto.Cipher import AES

# TODO: 优化结构

"""
解密部分原作者：https://github.com/CharlesPikachu
Function:
	用于算post的两个参数, 具体原理详见知乎：
	https://www.zhihu.com/question/36081767
"""

class Cracker():
    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'

    def get(self, text):
        text = json.dumps(text)
        secKey = self._createSecretKey(16)
        encText = self._aesEncrypt(self._aesEncrypt(text, self.nonce), secKey)
        encSecKey = self._rsaEncrypt(secKey, self.pubKey, self.modulus)
        post_data = {'params': encText, 'encSecKey': encSecKey}
        return post_data

    def _aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        text = text + str(pad * chr(pad))
        secKey = secKey.encode('utf-8')
        encryptor = AES.new(secKey, 2, b'0102030405060708')
        text = text.encode('utf-8')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext

    def _rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16)**int(
            pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def _createSecretKey(self, size):
        return (''.join(
            map(lambda xx: (hex(ord(xx))[2:]), str(os.urandom(size)))))[0:16]


class Wangyiyun():
    def __init__(self):
        self.headers = {
            'Accept':
            '*/*',
            'Accept-Encoding':
            'gzip,deflate,sdch',
            'Accept-Language':
            'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection':
            'keep-alive',
            'Content-Type':
            'application/x-www-form-urlencoded',
            'Host':
            'music.163.com',
            'cookie':
            '_iuqxldmzr_=32; _ntes_nnid=0e6e1606eb78758c48c3fc823c6c57dd,1527314455632; '
            '_ntes_nuid=0e6e1606eb78758c48c3fc823c6c57dd; __utmc=94650624; __utmz=94650624.1527314456.1.1.'
            'utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); WM_TID=blBrSVohtue8%2B6VgDkxOkJ2G0VyAgyOY;'
            ' JSESSIONID-WYYY=Du06y%5Csx0ddxxx8n6G6Dwk97Dhy2vuMzYDhQY8D%2BmW3vlbshKsMRxS%2BJYEnvCCh%5CKY'
            'x2hJ5xhmAy8W%5CT%2BKqwjWnTDaOzhlQj19AuJwMttOIh5T%5C05uByqO%2FWM%2F1ZS9sqjslE2AC8YD7h7Tt0Shufi'
            '2d077U9tlBepCx048eEImRkXDkr%3A1527321477141; __utma=94650624.1687343966.1527314456.1527314456'
            '.1527319890.2; __utmb=94650624.3.10.1527319890',
            'Origin':
            'https://music.163.com',
            'Referer':
            'https://music.163.com/',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.32 Safari/537.36'
        }
        self.player_url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        self.cracker = Cracker()

    # return music_play_url
    def get(self, music_url):
        songid = self.get_songid(music_url)
        params = {'ids': [songid], 'br': 320000, 'csrf_token': ''}
        data = self.__postRequests(self.player_url, params, 10)
        if data:
            url = data["data"][0]["url"]
            return url

    # 匹配出歌曲id
    def get_songid(self, music_url):
        pattern1 = re.compile(r'\?id=([0-9]*)', re.S)
        pattern2 = re.compile(r'song/([0-9]*?)/')
        if re.findall(pattern1, music_url):
            return int(re.findall(pattern1, music_url)[0])
        elif re.findall(pattern2, music_url):
            return int(re.findall(pattern2, music_url)[0])
        else:
            return int(music_url)

    def __postRequests(self, url, params, timeout):
        post_data = self.cracker.get(params)
        res = requests.post(url,
                            data=post_data,
                            timeout=timeout,
                            headers=self.headers)
        if res.json()['code'] != 200:
            return None
        else:
            return res.json()


def get(url: str) -> dict:
    data = {}
    wangyiyun = Wangyiyun()
    url = wangyiyun.get(url)
    if url:
        data["audios"] = [url]
    else:
        data["msg"] = "获取失败"

    return data


if __name__ == "__main__":
    print(get(input("url: ")))