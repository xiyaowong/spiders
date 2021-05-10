'''解析单个抖音视频的信息，链接形式应为: https://v.douyin.com/eU8msaG/'''
import re
from typing import Optional

import httpx
from pydantic import BaseModel, Field, HttpUrl

from .base import BaseResponseModel


class Video(BaseModel):
    play: HttpUrl = Field(..., description='视频播放地址')
    cover: HttpUrl = Field(..., description='视频封面')


class Music(BaseModel):
    play: HttpUrl = Field(..., description='音频地址')
    author: str = ''
    title: str = ''


class RequestModel(BaseModel):
    # https://v.douyin.com/eU8msaG/
    url: HttpUrl = Field(..., description='视频分享链接 v.douyin.com/*****')


class ResponseModel(BaseResponseModel):
    author: str = ''
    title: Optional[str]
    video: Optional[Video]
    music: Optional[Music]


async def process(request: RequestModel) -> ResponseModel:
    async with httpx.AsyncClient(
        headers={
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        },
        timeout=20,
    ) as client:
        # 短链接转长链接
        resp: httpx.Response = await client.get(request.url)
        if resp.status_code != 200:
            return ResponseModel(ok=False, msg='请求该地址出错')
        # 找到视频item_id
        if found := re.findall(r'video/(\d+)', str(resp.url)):
            item_id = found[0]
            resp = await client.get(
                f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={item_id}'
            )
            if resp.json()['status_code'] == 0:
                info = resp.json()["item_list"][0]
                data = {}
                data["author"] = info["author"]["nickname"]
                data["title"] = info["desc"]
                if 'music' in info:
                    data['music'] = Music(
                        play=info['music']['play_url']['uri'],
                        author=info['music']['author'],
                        title=info['music']['author'],
                    )
                data['video'] = Video(
                    play=info['video']['play_addr']['url_list'][0].replace(
                        'playwm', 'play'
                    ),
                    cover=info['video']['cover']['url_list'][0],
                )
                return ResponseModel(ok=True, **data)
        else:
            return ResponseModel(ok=False, msg='无法找到视频ID')
    return ResponseModel(ok=False, msg='获取失败')
