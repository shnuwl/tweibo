# -*- coding:utf-8 -*- #
#! /usr/bin/env python

import webbrowser

from oauth import OAuth2Handler
from tweibo import API

# 换成你的 APPKEY
APP_KEY = "801344987"
APP_SECRET = "1d030b22aefea54fc812bcfd5babe5ae"
CALLBACK_URL = "http://www.google.cn/"
# 在浏览器里打开地址来获得API权限
class Authorize:
    def tweibo_authorize(self):
        oauth = OAuth2Handler()
        oauth.set_app_key_secret(APP_KEY, APP_SECRET, CALLBACK_URL)
        webbrowser.open_new(oauth.get_access_token_url())
        responseData = raw_input(r"please input authorization information :")
        token_list = responseData.split("&")
        ACCESS_TOKEN = token_list[0][13:]
        OPENID = token_list[2][7:]
        oauth.set_access_token(ACCESS_TOKEN)
        oauth.set_openid(OPENID)
        return API(oauth)