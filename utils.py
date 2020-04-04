import os
import re
from datetime import datetime

import click
import requests


def filter_name(name):
    """
    过滤文件名
    """
    regexp = re.compile(r'(/|\\|:|\?|\*|\||"|\'|<|>|\$)')
    space = re.compile(r'\s{1,}')
    return space.sub("-", regexp.sub("", name))


def check_dir(path):
    """
    检查文件夹是否存在，存在返回True;不存在则创建，返回False
    """
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True


def download(file_url, file_name=None, file_type=None, save_path="download", headers=None):
    """
    :param file_url: 下载资源链接
    :param file_name: 保存文件名，默认为当前日期时间
    :param file_type: 文件类型(扩展名)，也是保存路径
    :param save_path: 保存路径，默认为download,后面不要"/"
    :param headers: http请求头，默认为iphone
    """
    if file_name is None:
        file_name = str(datetime.now())
    file_name = filter_name(file_name)

    if file_type is None:
        if "." in file_url:
            file_type = file_url.split(".")[-1]
        else:
            file_type = "uknown"

    check_dir(f"{save_path}/{file_type}")
    file_name = file_name + "." + file_type

    if headers is None:
        headers = {
            "User-Agent":
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1"
        }

    # 下载提示
    print(f"Downloading {file_name}")
    with requests.get(file_url, headers=headers, stream=True) as rep:
        file_size = int(rep.headers['Content-Length'])
        if rep.status_code != 200:
            print("下载失败")
            return False
        label = '{:.2f}MB'.format(file_size / (1024 * 1024))
        with click.progressbar(length=file_size, label=label) as progressbar:
            with open(f"{save_path}/{file_type}/{file_name}", "wb") as f:
                for chunk in rep.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        progressbar.update(1024)
        print("下载成功")
        return True
