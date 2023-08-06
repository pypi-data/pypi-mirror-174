# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@version    : v1.0
@author     : fangzheng
@contact    : fangzheng@rp-pet.cn
@software   : PyCharm
@filename   : WeChat.py
@create time: 2022/9/27 2:54 PM
@modify time: 2022/9/27 2:54 PM
@describe   : 
-------------------------------------------------
"""
import json
import requests


class WeChat:
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = self._getToken()

    def _getToken(self):
        try:
            if all([self.corpid, self.corpsecret]):
                url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}".format(
                    corpid=self.corpid, corpsecret=self.corpsecret)
                response = requests.get(url)
                if response.status_code == 200:
                    result = json.loads(response.text)
                    return result['access_token']
        except Exception as err:
            raise Exception("get WeChat access Token error", err)

    def _send_msg(self, data):
        self._check_token()
        try:
            send_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(
                access_token=self.access_token)
            response = requests.post(send_url, json.dumps(data))
            if response.status_code == 200:
                result = json.loads(response.text)
                return result
        except Exception as err:
            raise Exception("send WeChat Message error", err)

    def _check_token(self):
        if self.access_token is None:
            self._getToken()

    def send_msg(self, data):
        return self._send_msg(data)

    def send_text(self, data):
        return self._send_msg(data)

    def send_markdown(self, data):
        return self._send_msg(data)

    def send_image(self, data):
        return self._send_msg(data)

    def send_file(self, data):
        return self._send_msg(data)

    def send_textcard(self, data):
        return self._send_msg(data)
