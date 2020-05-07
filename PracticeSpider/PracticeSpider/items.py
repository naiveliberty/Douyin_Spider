# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Compose, TakeFirst
from PracticeSpider.utils.common import DouyinFontMap



class PracticespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# 清除字符串两边的空格
def clear_black(value):
    return "".join(value)


class DoyinUserInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


# douyin_user_tab
class DoyinUserInfoItem(scrapy.Item):
    nick_name = scrapy.Field(input_processor=MapCompose(clear_black))               # 用户昵称
    short_id = scrapy.Field(input_processor=Compose(DouyinFontMap.font_convert))    # 用户短 id
    uid = scrapy.Field(input_processor=Compose(lambda v: int(float(v[0]))))         # 用户 uid
    signature = scrapy.Field(input_processor=MapCompose(clear_black))               # 用户签名
    follow_nums = scrapy.Field(input_processor=Compose(DouyinFontMap.font_convert)) # 用户关注数
    fans_nums = scrapy.Field(input_processor=Compose(DouyinFontMap.font_convert))   # 用户粉丝数量
    likes_nums = scrapy.Field(input_processor=Compose(DouyinFontMap.font_convert))  # 用户获得赞的数量
    crawl_time = scrapy.Field()                                                     # 爬取时间

    def get_insert_sql(self):
        # douyin_user_tab 表中，uid 字段为唯一索引
        # 向 douyin_user_tab 插入之前，先查看是否存在 uid 相同的记录，如果存在更新指定字段，如果不存在就直接插入
        # 更新的字段为 nick_name、short_id、signature、follow_nums、fans_nums、likes_nums、crawl_time
        insert_sql = """
        insert into douyin_user_tab(nick_name, short_id, uid, signature, follow_nums, fans_nums, likes_nums,
        crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
        nick_name = VALUES(nick_name), short_id = VALUES(short_id), signature = VALUES(signature),
        follow_nums = VALUES(follow_nums), fans_nums = VALUES(fans_nums), likes_nums = VALUES(likes_nums),
        crawl_time = VALUES(crawl_time);
        """
        params = list()
        params.append(self.get("nick_name"))
        params.append(self.get("short_id"))
        params.append(self.get("uid"))
        params.append(self.get("signature"))
        params.append(self.get("follow_nums"))
        params.append(self.get("fans_nums"))
        params.append(self.get("likes_nums"))
        params.append(self.get("crawl_time"))
        return insert_sql, params


class DouyinUserVideoInfoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


# douyin_video_tab
class DouyinUserVideoInfoItem(scrapy.Item):
    uid = scrapy.Field()  # 用户 uid
    aweme_id = scrapy.Field()  # 视频 id
    info = scrapy.Field()  # 视频信息
    share_count = scrapy.Field()  # 视频分享数
    comment_count = scrapy.Field()  # 视频评论数
    like_count = scrapy.Field()  # 视频点赞数
    watemark_url = scrapy.Field()  # 有水印 url，PC 端可以直接访问
    unmark_url = scrapy.Field()  # 无水印 url，替换 User-agent 为移动端之后，可以正常访问
    localpath = scrapy.Field()  # 无水印视频下载完后，本地存放地址
    video_cover_url = scrapy.Field()  # 视频封面 url
    crawl_time = scrapy.Field()  # 爬取时间

    def get_insert_sql(self):
        # 在 douyin_video_tab 表中，为 aweme_id 字段创建了唯一索引
        # 向 douyin_video_tab 插入之前，先查看是否存在 aweme_id 相同的记录，如果存在更新指定字段，如果不存在就直接插入
        # 更新的字段为 info、share_count、comment_count、like_count、crawl_time
        insert_sql = """
        insert into douyin_video_tab(uid, aweme_id, info, share_count, comment_count, like_count, watemark_url,
        unmark_url, localpath, video_cover_url, crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE
        info = VALUES(info), share_count = VALUES(share_count), comment_count = VALUES(comment_count),
        like_count = VALUES(like_count), crawl_time = VALUES(crawl_time), localpath = VALUES(localpath);
        """
        params = list()
        params.append(self.get("uid"))
        params.append(self.get("aweme_id"))
        params.append(self.get("info"))
        params.append(str(self.get("share_count")))
        params.append(str(self.get("comment_count")))
        params.append(str(self.get("like_count")))
        params.append(self.get("watemark_url"))
        params.append(self.get("unmark_url"))
        params.append(self.get("localpath"))
        params.append(self.get("video_cover_url"))
        params.append(self.get("crawl_time"))
        return insert_sql, params