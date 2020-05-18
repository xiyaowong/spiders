import os
import re
import time
from datetime import datetime
from functools import wraps

import click
import requests


def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)


def filter_name(name):
    """
    过滤文件名
    """
    regexp = re.compile(r'(/|\\|:|\?|\*|\||"|\'|<|>|\$)')
    space = re.compile(r'\s{2,}')
    return space.sub(" ", regexp.sub("", name))


def check_dir(path):
    """
    检查文件夹是否存在，存在返回True;不存在则创建，返回False
    """
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True


def retry(n=3, delay=0.5):
    def deco(func):
        @wraps(func)
        def wrapper(*a, **kw):
            count = 1
            while True:
                try:
                    return func(*a, **kw)
                except Exception as e:
                    if count == n + 1:
                        break
                    print('[{}]运行错误，{}s后进行第{}次重试 Err: {}'.format(func.__name__, delay, count, e))
                    count += 1
                    time.sleep(delay)
            print('重试结束，[{}]运行失败'.format(func.__name__))
            return False
        return wrapper
    return deco


def download(file_url, file_name=None, file_type=None, save_path="download", headers=None, timeout=15):
    """
    :param file_url: 下载资源链接
    :param file_name: 保存文件名，默认为当前日期时间
    :param file_type: 文件类型(扩展名)
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

    check_dir(save_path)

    file_name = file_name + "." + file_type

    if headers is None:
        headers = {
            "User-Agent":
            "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1"
        }

    # 下载提示
    if os.path.exists(f"{save_path}/{file_name}"):
        print(f'\033[33m{file_name}已存在，不再下载！\033[0m')
        return True
    print(f"Downloading {file_name}")
    try:
        with requests.get(file_url, headers=headers, stream=True, timeout=timeout) as rep:
            file_size = int(rep.headers['Content-Length'])
            if rep.status_code != 200:
                print("\033[31m下载失败\033[0m")
                return False
            label = '{:.2f}MB'.format(file_size / (1024 * 1024))
            with click.progressbar(length=file_size, label=label) as progressbar:
                with open(f"{save_path}/{file_name}", "wb") as f:
                    for chunk in rep.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            progressbar.update(1024)
            print(f"\033[32m{file_name}下载成功\033[0m")
    except Exception as e:
        print('下载失败: ', e)
        remove_file(f"{save_path}/{file_name}")
    return True
