# -*- coding: utf-8 -*-
"""
@author: liberty
@file: douyin2.py
@time: 2021-05-25 16:20
@annotation: 注释
"""
import requests
import re


class DouYin:
    def __init__(self):
        self.url_list = ['https://v.douyin.com/e5qjGkg/', 'https://v.douyin.com/eP7Ndpj/']
        self.headers = {
            'authority': 'v.douyin.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }

    def get_sec_uid(self, url):
        res = requests.get(url, headers=self.headers, allow_redirects=False)
        location_url = res.headers['location']
        sec_uid_obj = re.search('sec_uid=(.*?)&', location_url)
        user_id_obj = re.search('user/(\d+)\?', location_url)
        if sec_uid_obj and user_id_obj:
            sec_uid = sec_uid_obj.group(1)
            user_id = user_id_obj.group(1)
            print(f'获取用户 sec_uid and user_id 成功：sec_uid: {sec_uid}  user_id:{user_id}')
            return sec_uid, user_id
        else:
            print('获取用户 sec_uid 失败')

    def get_signature(self, ua, user_id):
        params = {
            'ua': ua,
            'user_id': user_id
        }
        return requests.get('http://127.0.0.1:8000/douyin2', params=params).text

    def get_user_video(self, sec_uid, user_id):
        signature = self.get_signature(self.headers['user-agent'], user_id)
        url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/'
        params = {
            'sec_uid': sec_uid,
            'count': '21',
            'max_cursor': '0',
            'aid': '1128',
            '_signature': signature,
            'dytk': '',
        }
        headers = {
            'authority': 'www.iesdouyin.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'accept': 'application/json',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.iesdouyin.com/share/user/67502228856?sec_uid=MS4wLjABAAAAYIN1c9oIG_oCZuDe2rYbRdfXs86P9hMhoFW4pMq3FZU&did=MS4wLjABAAAAxAEGb4hFIguGXQurlNVqYqYO1tvdaqVCUTiSgDXAObM&iid=MS4wLjABAAAAEE9BFybq-cr1XU0U2b7sqKQ387Hdx63S_8uxDs8SMVqBCBpqMPImxhHtWnqzEQZj&with_sec_did=1&u_code=153dadji8&timestamp=1621930512&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_app_name=douyin',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        while True:
            res = requests.get(url, headers=headers, params=params)
            res_dc = res.json()
            for i in res_dc['aweme_list']:
                print(i['desc'])
                print(i['video']['play_addr']['url_list'][0])
            if res_dc['has_more']:
                max_cursor = res_dc['max_cursor']
                params['max_cursor'] = max_cursor
            else:
                break

    def run(self):
        for url in self.url_list:
            result = self.get_sec_uid(url)
            if result:
                self.get_user_video(*result)


if __name__ == '__main__':
    dy = DouYin()
    dy.run()