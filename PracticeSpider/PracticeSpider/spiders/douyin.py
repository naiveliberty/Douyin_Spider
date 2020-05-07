# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import FormRequest
import re
from PracticeSpider.items import DouyinUserVideoInfoItemLoader, DoyinUserInfoItemLoader, DoyinUserInfoItem, \
    DouyinUserVideoInfoItem
from datetime import datetime
import codecs


class DouyinSpider(scrapy.Spider):
    name = 'douyin'
    allowed_domains = ['douyin.com', '127.0.0.1']
    start_urls = ['http://www.douyin.com/share/user/56874100517','http://www.douyin.com/share/user/67502228856',
                  'http://www.douyin.com/share/user/108260651337']

    def parse(self, response):
        item_loader = DoyinUserInfoItemLoader(item=DoyinUserInfoItem(), response=response)
        # 用户昵称
        item_loader.add_xpath("nick_name", "//p[@class='nickname']/text()")
        # 用户短 id
        item_loader.add_xpath("short_id", "//p[@class='shortid']/i/text()")
        # 用户签名
        item_loader.add_xpath("signature", "//p[@class='signature']/text()")
        # 用户关注数
        item_loader.add_xpath("follow_nums", "//span[@class='focus block']/span[@class='num']/i/text()")
        # 用户粉丝数量
        item_loader.add_xpath("fans_nums", "//span[@class='follower block']/span[@class='num']//text()")
        # 用户获得赞的数量
        item_loader.add_xpath("likes_nums", "//span[@class='liked-num block']/span[@class='num']//text()")
        # 爬取时间
        item_loader.add_value("crawl_time", datetime.now())

        html = response.text
        # 正则匹配用户 uid
        uid_res = re.search('uid: "(\d+)"', html, re.S)
        # 正则匹配用户 token
        token_res = re.search("dytk: '(.+?)'", html, re.S)
        # 正则匹配 tac 字段
        tac_res = re.search("<script>.*?tac='(.*?)'</script>", html, re.S)
        if uid_res and token_res and tac_res:
            # 用户 uid
            item_loader.add_xpath("uid", uid_res.group(1))
            yield item_loader.load_item()

            params = {
                "uid": uid_res.group(1),
                "tac": codecs.getdecoder("unicode_escape")(tac_res.group(1).encode())[0],
            }

            data = {
                "uid": uid_res.group(1),
                "token": token_res.group(1)
            }
            local_node_server = 'http://127.0.0.1:8000/douyin'

            yield FormRequest(url=local_node_server, formdata=params, method="GET", meta= data, callback=self.parse_video_request)

    def parse_video_request(self, response):
        # meta 中包含了 "uid", "token"
        meta = response.meta
        video_info_api = "https://www.douyin.com/web/api/v2/aweme/post/"
        video_params = {
            # 用户 id
            'user_id': meta['uid'],
            # 加密 uid，本接口下默认为空
            'sec_uid': '',
            # 请求数量，固定值不变，
            'count': "21",
            # 本次请求视频最大值，可从上一次请求的 response 中获取，初始为 0
            'max_cursor': "0",
            # appid 固定不变
            'aid': "1128",
            # 加密签名
            '_signature': "",
            # 用户 token
            'dytk': meta["token"]
        }
        # 如果 "web/api/v2/aweme/post" 存在与 response.url 说明这个是 >= 2 次请求指定博主的视频信息
        if "web/api/v2/aweme/post" in response.url:
            video_params["_signature"] = meta["_signature"]
            video_dc = response.text
            result = json.loads(video_dc)
            aweme_list = result["aweme_list"]
            for video in aweme_list:
                item_loader = DouyinUserVideoInfoItemLoader(DouyinUserVideoInfoItem(), selector=video)
                item_loader.add_value("uid", video["author"]["uid"])
                item_loader.add_value("aweme_id", video["aweme_id"])
                item_loader.add_value("info", video["desc"])
                item_loader.add_value("share_count", video["statistics"]["share_count"])
                item_loader.add_value("comment_count", video["statistics"]["comment_count"])
                item_loader.add_value("like_count", video["statistics"]["digg_count"])
                item_loader.add_value("watemark_url", video["video"]["play_addr"]["url_list"][0].replace("play", "playwm", 1))
                item_loader.add_value("unmark_url", video["video"]["play_addr"]["url_list"][0])
                item_loader.add_value("video_cover_url", video["video"]["dynamic_cover"]["url_list"][0])
                item_loader.add_value("crawl_time", datetime.now())
                yield item_loader.load_item()
            # 获取 max_cursor 为下次请求做准备
            max_cursor = result['max_cursor']
            # 获取 has_more 参数，判断是否为最后一条请求
            has_more = result['has_more']

            if has_more:
                video_params['max_cursor'] = str(max_cursor)
                yield FormRequest(url=video_info_api, formdata=video_params, method="GET", meta=meta, callback=self.parse_video_request)
        else:
            # 第一次请求用户视频信息
            # 向本地 nodejs 服务器发送请求，获取抖音加密参数
            _signature = response.text
            # 将 _signature 值添加进 meta 中，传递给下一次请求使用，每个博主的账号每次只用请求一次 nodejs 服务器，来获取 _signature
            video_params["_signature"] = _signature
            meta["_signature"] = _signature
            yield FormRequest(url=video_info_api, formdata=video_params, method="GET", meta=meta, callback=self.parse_video_request)



