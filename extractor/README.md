### 这里是一些小爬虫集合

---

每个平台对应一个文件，每个文件里面有一个`get(url: str)`函数 统一形式如下(里面使用 f-string 需要 python3.6+)：

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
    ☆ 爬取未成功也会返回data，而且不一定为空
"""
```

# 默认输入的链接都正确:grin:

---

|          平台          |       资源内容       |      完成状态      |
| :--------------------: | :------------------: | :----------------: |
|   bilibili(哔哩哔哩)   |      封面、视频      | :white_check_mark: |
|     changya(唱鸭)      |         音频         | :white_check_mark: |
|      douyin(抖音)      |      无水印视频      | :white_check_mark: |
|      kugou(酷狗)       |         音频         | :white_check_mark: |
|       kuwo(酷我)       |         音频         | :white_check_mark: |
|    lizhiFM(荔枝 FM)    |         音频         | :white_check_mark: |
|  music163(网易云音乐)  |    音频、视频、mv    | :white_check_mark: |
|    qqmusic(QQ 音乐)    |         音频         | :white_check_mark: |
| pipigaoxiao(皮皮搞笑)  |      无水印视频      | :white_check_mark: |
| quanminkge(全民 K 歌)  |      音频或视频      | :white_check_mark: |
|      weibo(微博)       |         视频         | :white_check_mark: |
|      weishi(微视)      |      无水印视频      | :white_check_mark: |
|      zhihu(知乎)       |         视频         | :white_check_mark: |
|   zuiyou_voice(最右)   |   音频(语音帖评论)   | :white_check_mark: |
|   zuiyou_video(最右)   |         视频         | :white_check_mark: |
|   qianqian(千千音乐)   |         音频         | :white_check_mark: |
|      5sing(5sing)      |         音频         | :white_check_mark: |
|     pipix(皮皮虾)      |      无水印视频      | :white_check_mark: |
|   qingshipin(轻视频)   |      无水印视频      | :white_check_mark: |
|   qutoutiao(趣头条)    |         视频         |       :dash:       |
|      ku6(酷 6 网)      |         视频         | :white_check_mark: |
|      lofter(乐乎)      |         视频         | :white_check_mark: |
|  open163(网易公开课)   |       免费视频       | :white_check_mark: |
|  xinpianchang(新片场)  |         视频         | :white_check_mark: |
|  baidutieba(百度贴吧)  |         视频         | :white_check_mark: |
|     kuaishou(快手)     | 无水印视频、长图视频 | :white_check_mark: |
|  acfun(AcFun 弹幕网)   |         视频         | :white_check_mark: |
|  haokan(百度好看视频)  |         视频         | :white_check_mark: |
|   pearvideo(梨视频)    |         视频         | :white_check_mark: |
|   xiaokaxiu(小咖秀)    |      无水印视频      | :white_check_mark: |
|    sohuTV(搜狐视频)    |         视频         | :white_check_mark: |
|        ted(TED)        |         视频         | :white_check_mark: |
|    tudou(土豆视频)     |         视频         | :white_check_mark: |
| quanminxsp(全民小视频) |         视频         | :white_check_mark: |
|       lequ(乐趣)       |    背景动图、音频    | :white_check_mark: |
|   peiyinxiu(配音秀)    |         视频         | :white_check_mark: |
|     tuchong(图虫)      |         图片         | :white_check_mark: |
|     changba(唱吧)      |         视频         | :white_check_mark: |
|     migu(咪咕音乐)     |         音频         | :white_check_mark: |
|       momo(陌陌)       |         视频         | :white_check_mark: |
