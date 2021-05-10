'''解析快手无水印视频或长图视频，链接应为https://v.kuaishou.com/****'''
import json
import re
from typing import List

import httpx
from pydantic import BaseModel, Field, HttpUrl

from .base import BaseResponseModel


class RequestModel(BaseModel):
    url: HttpUrl = Field(..., description='快手分享链接')


class ResponseModel(BaseResponseModel):
    title: str = ''
    video: HttpUrl = Field(None, description='视频链接')
    image: List[HttpUrl] = Field(None, description='长图视频的图片链接')


async def process(request: RequestModel):
    # 如果是桌面端的链接，需要改一下
    url = request.url
    # FIXME: 这里是直接复制的原先的处理方式，实际上是有问题的
    # 有空修复 所以尽量只接受短链接的分享链接 https://v.kuaishou.com/***
    if temp := re.findall(r'live\.kuaishou\.com/u/\w+/(\w+)', url):
        url = f'https://c.kuaishou.com/fw/photo/{temp[0]}'
    async with httpx.AsyncClient(
        headers={
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25",
            "Cookie": "did=web_68e0268146694843a92700d2de49a0a6;",
        },
        timeout=20,
    ) as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            if page_data_str := re.findall(
                r'<script type="text/javascript">window\.pageData= (\{.*?\})</script>',
                resp.text,
            ):
                try:
                    page_data = json.loads(page_data_str[0])
                except Exception:
                    return ResponseModel(ok=False, msg='解析网页数据失败')
                else:
                    data = {}
                    video_info = page_data['video']
                    data['title'] = video_info['caption']
                    if srcNoMark := video_info.get('srcNoMark'):
                        data['video'] = srcNoMark
                    if images := video_info.get('images'):
                        imageCDN = video_info.get('imageCDN')
                        if not imageCDN.startswith('http'):
                            imageCDN = 'http://' + imageCDN
                        data['image'] = [imageCDN + image['path'] for image in images]
                    return ResponseModel(ok=True, **data)
            else:
                return ResponseModel(ok=False, msg='获取网页数据失败')
    return ResponseModel(ok=False, msg='获取失败')
