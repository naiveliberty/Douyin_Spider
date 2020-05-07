import re
import codecs
import time

import requests


class DouyinVideoInfo():
    def __init__(self, user_id):
        # 用户 id
        self.user_id = str(user_id)
        # 用户主页 url
        self.user_index_url = f"https://www.douyin.com/share/user/{self.user_id}"
        # 视频信息接口
        self.video_info_url = "https://www.douyin.com/web/api/v2/aweme/post/"
        # 请求超时时间
        self.timeout = 10
        # 页面 tac 值
        self.tac = ''
        # 用户 token
        self.dytk = ''
        # 加密签名
        self._signature = ''
        # 请求头
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        # 视频信息列表
        self.video_list = list()

    # 正则提取 tac 和 dytk 函数
    def extract_tac_dytk(self, res):
        result_tac = re.search("<script>.*?tac='(.*?)'</script>", res, re.S)
        result_dytk = re.search("dytk: '(.*?)'", res, re.S)
        if result_tac and result_dytk:
            return {"tac": result_tac.group(1), "dytk": result_dytk.group(1)}
        else:
            return

    # 页面获取 tac 和 dytk
    def get_tac_dytk(self):

        try:
            res = requests.get(self.user_index_url, headers=self.headers, timeout=self.timeout)
        except:
            print("网络异常，请求个人主页时出错！")
            return
        res.encoding = 'utf8'
        result = self.extract_tac_dytk(res.text)
        if result:
            # 恢复 tac 字符串中转义字符转义功能
            self.tac = codecs.getdecoder("unicode_escape")(result['tac'].encode())[0]
            self.dytk = result['dytk']
            return True
        else:
            print("提取tac和dytk异常，请检查页面布局是否变化")
            return

    # 获取视频信息
    def get_vidoe_info(self):
        # 本地 nodejs 服务，用于运行 js 代码，生成对应的加密参数
        local_server = 'http://127.0.0.1:8000/douyin'
        params = {
            'user_id': self.user_id,
            'tac': self.tac
        }
        try:
            res = requests.get(local_server, params=params)
        except:
            print("本地 nodejs 服务器异常，获取 _signature 失败！")
            return
        # 更新 _signature
        self._signature = res.text
        video_params = {
            # 用户 id
            'user_id': self.user_id,
            # 加密 uid，本接口下默认为空
            'sec_uid': '',
            # 请求数量，固定值不变，
            'count': 21,
            # 本次请求视频最大值，可从上一次请求的 response 中获取，初始为 0
            'max_cursor': 0,
            # appid 固定不变
            'aid': 1128,
            # 加密签名
            '_signature': self._signature,
            # 用户 token
            'dytk': self.dytk
        }
        while True:
            time.sleep(0.5)
            try:
                res = requests.get(self.video_info_url, headers=self.headers, params=video_params, timeout=self.timeout)
            except:
                print(f"请求视频接口异常已跳过，当前请求参数为{video_params}")
                continue
            result = res.json()
            # 获取视频详情列表
            aweme_list = result["aweme_list"]
            for video in aweme_list:
                print(
                    f'watermark: True, video_name: {video["desc"]}, video_url: {video["video"]["play_addr"]["url_list"][0].replace("play", "playwm", 1)}')
                self.video_list.append(
                    {"watermark": True, "video_name": video["desc"],
                     "video_url": video["video"]["play_addr"]["url_list"][0]})
            # 获取 max_cursor 为下次请求做准备
            max_cursor = result['max_cursor']
            # 获取 has_more 参数，判断是否为最后一条请求
            has_more = result['has_more']
            if has_more:
                video_params['max_cursor'] = max_cursor
            else:
                break

    # 获取无水印视频
    def get_not_watermark(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        for video in self.video_list:
            num = 0
            while True:
                try:
                    # 禁止重定向，视频真实地址在 response.headers['location'] 中
                    res = requests.get(video['video_url'], headers=headers, allow_redirects=False)
                except:
                    print(f"请求无水印视频异常已跳过，url：{video['video_url']}")
                    break
                # 如果状态码为 302，获取无水印视频地址，跳出循环
                if res.status_code == 302:
                    video["video_url"] = res.headers['location']
                    video["watermark"] = False
                    print(video)
                    break
                print(f"第{num}次请求无水印视频!")
                num += 1
                # 状态码为 200 时表明获取失败，阻塞0.5秒后重新发送
                time.sleep(0.5)

    def main(self):
        # 如果成功获取到 tac 和 dytk，就开始获取视频信息
        if self.get_tac_dytk():
            self.get_vidoe_info()
            # 获取无水印视频
            self.get_not_watermark()


if __name__ == "__main__":
    user_id = 56874100517
    douyin = DouyinVideoInfo(user_id)
    douyin.main()
