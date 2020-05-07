# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import os
import time

import MySQLdb.cursors
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
from PracticeSpider.items import DouyinUserVideoInfoItem
import scrapy

class PracticespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class VideoPipeline(object):
    def __init__(self, video_store):
        self.video_store = video_store

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            video_store=crawler.settings.get('VIDEO_STORE'),
        )

    def process_item(self, item, spider):
        if isinstance(item, DouyinUserVideoInfoItem):
            video_url = item["unmark_url"]
            temp_name = hashlib.md5(item["unmark_url"].encode("utf8")).hexdigest() + ".mp4"
            current_time = time.strftime('%Y%m%d', time.localtime())
            file_name = "/".join([self.video_store, current_time, temp_name])
            if not os.path.exists(file_name):
                request = scrapy.Request(video_url)
                dfd = spider.crawler.engine.download(request, spider)
                dfd.addBoth(self.download_video, item)
                return dfd
            else:
                item["localpath"] = file_name
        return item

    def download_video(self, response, item):
        temp_name = hashlib.md5(item["unmark_url"].encode("utf8")).hexdigest()+".mp4"
        current_time = time.strftime('%Y%m%d', time.localtime())
        file_name = "/".join([self.video_store, current_time, temp_name])
        path = "/".join([self.video_store, current_time])
        print(file_name)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(file_name, "wb") as f:
            f.write(response.body)
        item["localpath"] = file_name
        return item



class MySQLTwistedPipline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            port=settings["MYSQL_PORT"],
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用 twisted 将 mysql 插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # 处理异常插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的 item 构造不同 sql 语句进行插入 mysql 中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, tuple(params))