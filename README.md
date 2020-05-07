# douyin_spider

### 声明：项目内容不得用于商业用途，仅做学习交流，如果侵犯了您的利益和权益,请邮箱联系我，我将删除该项目。

| 作者    | 邮箱                                                |
| ------- | --------------------------------------------------- |
| liberty | [fthemuse@foxmail.com](mailto:fthemuse@foxmail.com) |

### 新增 Scrapy实现

#### 介绍

批量爬取抖音视频

#### 项目架构
1. 使用 Python 编写爬虫部分；
2. 使用 Node.js 执行 js 代码，生成加密参数，通过 web 服务的形式，提供给爬虫文件使用；

#### 目录结构

```
douyin.py				      #爬虫文件
douyin_signature.js		#抖音 _signature 参数生成文件
get_signa.js			    #express web框架入口文件
```

#### 签名生成需要的参数

```
tac			  # 可以从 PC 端用户主页 HTMl 源码中获取到
user_id		# 用户主页 url 中获取
userAgent	# 请求头中获取

#douyin_signature.js
该文件中的 userAgent 要和 douyin.py 中的 self.headers 保持一致，否则生成到 _signature 不可用
```

#### 无水印视频

获取到有水印视频地址之后，更换 userAgent 为移动端，发起请求，即可获取无水印视频。

#### 运行环境

```
Python 3.7
NodeJs 12.16.1
```

#### 环境依赖库

##### Python

- requests

#### NodeJs

- express
- jsdom
- canvas

#### 使用说明

1.  使用 `Nodejs` 运行 `get_signa.js`，启动 `web`服务；
2.  执行 `douyin.py`开始爬取。

