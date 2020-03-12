### 这里是一些小爬虫集合
---
每个平台对应一个文件，每个文件里面有一个`get(url: str)`函数 统一形式如下：
```python
"""
Args:
    url: str
Returns:
    data: dict
      |_ {
            title: str,
            author: str,
            audioName: str,
            videoName: str,
            imgs: List[str],
            audios: List[str],
            videos: List[str],
            text: str,
            msg: str
         }
Tips:
    data里面的各个字段只有当爬取到相关内容时才会存在，除了msg(不过这个没啥大用)
    ☆爬取未成功也会返回data，而且不一定为空
"""
```
# 默认输入的链接都正确:grin:
---

平台 | 资源内容 | 完成状态
:---:|:---:|:--:|
bilibili(哔哩哔哩) | 封面、视频 | :white_check_mark:
changya(唱鸭) | 音频 | :white_check_mark:
douyin(抖音) | 无水印视频 | :white_check_mark: |
kugou(酷狗) | 音频 | :white_check_mark: |
kuwo(酷我) | 音频 | :white_check_mark: |
lizhiFM(荔枝FM) | 音频 | :white_check_mark: |
music163(网易云音乐) | 音频 |:white_check_mark:|
qqmusic(QQ音乐) | 音频 | :white_check_mark: |
pipigaoxiao(皮皮搞笑) | 无水印视频 | :white_check_mark: |
quanminkge(全民K歌) | 音频或视频 | :white_check_mark:|
weibo(微博) | 视频 |:white_check_mark: |
weishi(微视) | 无水印视频 | :white_check_mark: |
zhihu(知乎) | 视频 |:white_check_mark: |
zuiyou(最右) | 音频(语音帖评论) |:white_check_mark: |
qianqian(千千音乐) | 音频 |:white_check_mark: |
5sing(5sing) | 音频 |:white_check_mark: |