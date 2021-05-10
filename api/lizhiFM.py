'''链接格式应为https://www.lizhi.fm/***/******'''
import re

import httpx
from pydantic import BaseModel, Field, HttpUrl

from .base import BaseResponseModel


class RequestModel(BaseModel):
    url: HttpUrl = Field(..., description='单个音频链接地址')


class ResponseModel(BaseResponseModel):
    author: str = None
    voice_name: str = None
    voice_url: HttpUrl = None


async def process(request: RequestModel) -> ResponseModel:
    # voice_id
    if voice_id := re.findall(r"/(\d+)", request.url):
        if len(voice_id) >= 2:
            voice_id = voice_id[1]
        else:
            voice_id = voice_id[0]
        async with httpx.AsyncClient(
            headers={
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
            },
            timeout=20,
        ) as client:
            resp = await client.get(f'https://m.lizhi.fm/vodapi/voice/info/{voice_id}')
            if resp.status_code == 200 and resp.json()['code'] == 0:
                info = resp.json()['data']['userVoice']
                return ResponseModel(
                    ok=True,
                    author=info['userInfo']['name'],
                    voice_name=info['voiceInfo']['name'],
                    voice_url=info['voicePlayProperty']['trackUrl'],
                )
            else:
                return ResponseModel(ok=False, msg=resp.json()['msg'])
    else:
        return ResponseModel(ok=False, msg='从链接获取音频ID失败')
    return ResponseModel(ok=False, msg='获取失败')
