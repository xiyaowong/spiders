import re

import execjs
import requests

js_code = """l=new Array(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,63,52,53,54,55,56,57,58,59,60,61,-1,-1,-1,-1,-1,-1,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,-1,-1,-1,-1,-1,-1,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1,-1);function u(t){var e,o,n,a,i,r,s;for(r=t.length,i=0,s="";i<r;){for(;e=l[255&t.charCodeAt(i++)],i<r&&-1==e;);if(-1==e)break;for(;o=l[255&t.charCodeAt(i++)],i<r&&-1==o;);if(-1==o)break;s+=String.fromCharCode(e<<2|(48&o)>>4);do{if(61==(n=255&t.charCodeAt(i++)))return s;n=l[n]}while(i<r&&-1==n);if(-1==n)break;s+=String.fromCharCode((15&o)<<4|(60&n)>>2);do{if(61==(a=255&t.charCodeAt(i++)))return s;a=l[a]}while(i<r&&-1==a);if(-1==a)break;s+=String.fromCharCode((3&n)<<6|a)}return s}"""
js = execjs.compile(js_code)


def get(url: str) -> dict:
    """
    videos
    """
    data = {}
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    rep = requests.get(url, headers=headers, timeout=10)
    if rep.status_code != 200:
        return {"msg": "获取失败"}

    enc_video_url = re.findall(r"video_url: '(.*?)',", rep.text)[0]
    video_url = "https:" + js.call("u", (enc_video_url,))
    data["videos"] = [video_url]
    return data


if __name__ == "__main__":
    print(get(input("url: ")))
