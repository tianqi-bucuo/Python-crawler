#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re

# 第一步：访问登陆页,拿到X_Anti_Forge_Token，X_Anti_Forge_Code
# 1、请求url:https://passport.lagou.com/login/login.html
# 2、请求方法:GET
# 3、请求头:
#    User-agent
r1 = requests.get(
    url='https://passport.lagou.com/login/login.html',
    headers={
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 "
                      "(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/" "537.36"
            },
                 )
#
# X_Anti_Forge_Token = re.findall("X_Anti_Forge_Token = '(.*?)'", r1.text, re.S)[0]
# X_Anti_Forge_Code = re.findall("X_Anti_Forge_Code = '(.*?)'", r1.text, re.S)[0]
# print(X_Anti_Forge_Token, X_Anti_Forge_Code)
# print(r1.cookies.get_dict())
# 第二步：登陆
# 1、请求url:https://passport.lagou.com/login/login.json
# 2、请求方法:POST
# 3、请求头:
#    cookie
#    User-agent
#    Referer:https://passport.lagou.com/login/login.html
#    X-Anit-Forge-Code:53165984
#    X-Anit-Forge-Token:3b6a2f62-80f0-428b-8efb-ef72fc100d78
#    X-Requested-With:XMLHttpRequest
# 4、请求体：
# isValidate:true
# username:15131252215
# password:ab18d270d7126ea65915c50288c22c0d
# request_form_verifyCode:''
# submit:''
# r2 = requests.post(
#     'https://passport.lagou.com/login/login.json',
#     headers={
#         'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 "
#                       "(KHTML, like Gecko) Chrome/73.0.3683.103 Safari/" "537.36",
#         'Referer': 'https://passport.lagou.com/login/login.html',
#         'X-Anit-Forge-Code': X_Anti_Forge_Code,
#         'X-Anit-Forge-Token': X_Anti_Forge_Token,
#         'X-Requested-With': 'XMLHttpRequest'
#     },
#     data={
#         "isValidate": True,
#         'username': '15131255089',
#         'password': 'ab18d270d7126ea65915c50288c22c0d',
#         'request_form_verifyCode': '',
#         'submit': ''
#     },
#     cookies=r1.cookies.get_dict()
# )
# print(r2.text)
#
