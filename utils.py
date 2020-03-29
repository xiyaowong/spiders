import os
from datetime import datetime

import requests


def download(url, file_name=None, file_type=None, headers=None):
    """
    Args:
        url: 下载资源链接
        file_name: 保存文件名，默认为当前日期时间
        file_type: 文件扩展名，有的话就单独创建文件夹
        headers: http请求头，默认为iphone
    """
    if not os.path.exists("download"):
        os.mkdir('download')

    if file_name is None:
        file_name = str(datetime.now())
    file_name = file_name.replace("\\", "").replace("/", "").replace("#", "")

    if file_type is not None:
        if not os.path.exists(f"download/{file_type}"):
            os.mkdir(f"download/{file_type}")
        file_name = file_type + "/" + file_name + "." + file_type
    else:
        file_type = ""

    if headers is None:
        headers = {
            "User-Agent":
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1"
        }

    rep = requests.get(url, headers=headers, stream=True)
    rep.raise_for_status()

    content_length = int(rep.headers['Content-Length'])
    count = 1024
    with open(f"download/{file_name}", 'wb') as file:
        print("=================================================")
        print('正在下载{}，大小为：{:.2}m'.format(file_name, (content_length / 1024.0 / 1024)))
        for chunk in rep.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                print('{}/100\r'.format(int(count * 100 / content_length)), end='', flush=True)
                count += 1024
        print(f'{file_name}下载成功')
        print("=================================================")


if __name__ == "__main__":
    url = "https://cn-hncs-gd-bcache-08.bilivideo.com/upgcxcode/50/22/151882250/151882250-1-16.mp4?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1581866986&gen=playurl&os=bcache&oi=1999373771&trid=eb5d3963b9e148acb4bd960343a5f9e4h&platform=html5&upsig=b2251c540a8d5765cceee48b89887fa2&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&origin_cdn=ks3"
    file = "test.mp4"
    download(url, file)
