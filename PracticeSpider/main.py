from scrapy.cmdline import execute

import os
import sys
import time
# 将项目根录添加到 path 系统环境中，防止使用命令运行项目时，发生导包错误
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy', 'crawl', 'douyin'])

