#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import requests
import json
import sys

baidu = 'http://www.baidu.com/'
# change this to file you want to save login info
info_file = '/path/to/save/cmcc_info.json'
username = 'your telephone number'
password = 'your static password'


r = requests.get(baidu)
url = r.url
if url == baidu:
    domain = ''
    login_info = {}
    print '正在下线...'
else:
    print '正在登录...'
    domain, args_url = url.split('?')
    wlanacssid = 'CMCC-EDU'     # for CMCC-EDU, ssid is always CMCC-EDU
    args = args_url.split('&')
    for arg in args:
        if arg.split('=')[0] == 'wlanuserip':
            wlanuserip = arg.split('=')[1]
        elif arg.split('=')[0] == 'wlanacname':
            wlanacname = arg.split('=')[1]
        elif arg.split('=')[0] == 'wlanacip':
            wlanacip = arg.split('=')[1]
        # elif arg.split('=')[0] == 'wlanacssid':
        #     wlanacssid = arg.split('=')[1]
    login_info = {
        'staticusername':username,
        'staticpassword':password,
        'wlanacname':wlanacname,
        'wlanuserip':wlanuserip,
        'loginmode':'static',
        'wlanacssid':wlanacssid
    }
    logout_info = {
        'username':username,
        'wlanacname':wlanacname,
        'wlanuserip':wlanuserip,
        'wlanacssid':wlanacssid
    }
    info = {'domain':domain, 'logout_info':logout_info}
    with open(info_file, 'w') as f:
        json.dump(info, f)

    
def login(domain,info):
    url = domain.replace('input', 'login')
    r = requests.post(url,info)
    encoding = r.encoding
    content = r.content.decode(encoding)
    if '登录成功' in content:
        print '登录成功！下线请运行命令: python cmcc_edu.py logout'
    else:
        print '登录失败！'

def logout(domain,info):
    url = domain.replace('input', 'logout')
    requests.post(url,info)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'login':
            login(domain, login_info)
        if sys.argv[1] == 'logout':
            with open(info_file, 'r') as f:
                d = json.load(f)
            domain = d['domain']
            logout_info = d['logout_info']
            logout(domain, logout_info)
    else:
        print """Invalid command. Please use
        ``python cmcc_edu.py login`` to login
        ``python cmcc_edu.py logout`` to logout"""
