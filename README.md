# douyin_spider

**声明：项目内容不得用于商业用途，仅做学习交流，如果侵犯了您的利益和权益,请邮箱联系我，我将删除该项目。**

**声明：项目内容不得用于商业用途，仅做学习交流，如果侵犯了您的利益和权益,请邮箱联系我，我将删除该项目。**

**声明：项目内容不得用于商业用途，仅做学习交流，如果侵犯了您的利益和权益,请邮箱联系我，我将删除该项目。**

| 作者    | 邮箱                                                |
| ------- | --------------------------------------------------- |
| liberty | [fthemuse@foxmail.com](mailto:fthemuse@foxmail.com) |

### 

#### 介绍

批量爬取抖音web个人主页视频

#### 项目架构
1. 使用 Python 编写爬虫部分；
2. 使用 Node.js 执行 js 代码，生成加密参数，通过 web 服务的形式，提供给爬虫文件使用；

#### 目录结构

- ~~douyin.py~~ （已失效）和 douyin2.py（爬虫文件）
- get_signa.js（express web框架入口文件）
- ~~douyin_signature.js~~（已失效） 和 douyin_signature2.js 为  _signature 生成算法

#### 环境依赖库

##### Python

- requests

#### NodeJs

- express
- jsdom
- canvas

#### 使用说明

1.  使用 `Nodejs` 运行 `get_signa.js`，启动 `web`服务；
2.  执行 `douyin2.py`开始爬取。

