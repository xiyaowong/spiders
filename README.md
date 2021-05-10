# 使用 fastAPI 构建一个简单的解析接口

此项目代码倾向于初学者学习或了解爬虫,
缺乏很多必要的校验，也没有请求速率控制、接口权限校验等等必要的功能，
仅适用于搭建自用接口，满足日常的需求

代码本身并没有很多可以阅读的地方，因为每个平台的信息都是不同的，
具体信息需要自己得到链接然后找接口，平时也不可能有这么多平台的需求,
所以随便看两个就差不多了。

这里简单讲一下项目思路

选择 fastAPI 是因为这个框架实在是太方便了。有其他 web 框架基础，入门 fastAPI 是零成本的。
本项目使用到的特性也非常少，所以看完 fastAPI 文档中介绍的几个基础示例就够了。

文件夹(包)`api`中包含了各个平台的处理模块，每个模块需要定义`RequestModel`类
`ResponseModel`类 `process`函数

- process 是每个爬虫的视图函数
- RequestModel 是用于解析请求体的，由 fastAPI 自动处理
- ResponseModel 是视图函数返回的类型，也是对应接口返回的结构，用于定义注册路由中的
  `response_model`参数

在`main.py`中，扫描 api 文件夹中的文件，对文件名进行简单的筛选处理，再动态导入各个爬虫模块，
模块名称作为接口路由名(path)，模块文档(`__doc__`)作为路由说明(description)

# 如何运行

为了简单，本项目零配置项。使用`poetry`进行包管理

```shell
poetry install
poetry run uvicorn main:app
```

或者使用常规方法(python>=3.8)

```shell
pip install -r requirements.txt
ucicorn main:app
```

然后访问控制台提示的服务地址即可
