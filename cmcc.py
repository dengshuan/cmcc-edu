#!/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import unicode_literals
import urllib, urllib2, sys, json, re

baidu = 'http://www.baidu.com'
# change this to file you want to save login info
info_file = '/path/to/save/cmcc_info.json'
username = 'your telephone number'
password = 'your static password'

def get_info(site=baidu):
    request = urllib2.urlopen(baidu)
    url = request.url                   # get redirect url
    if url == site:
        domain = ''
        login_info = {}
        print '已经连网，不用再登录了:-)'
    else:
        print '正在获取登录信息...'
        domain, args_url = url.split('?')
        wlanacssid = 'CMCC-EDU' # for CMCC-EDU, ssid is always CMCC-EDU
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
    return domain, login_info



def login(domain, info):
    if domain:
        print '正在登录...'
        params = urllib.urlencode(info)
        login_url = domain.replace('input', 'login')
	# uncheck certificate,this is unsafe, as soon as CMCC-EDU 
	# certificate be valid again, you should set verify=True for
	# security
        request = urllib2.Request(url=login_url, data=params, unverifiable=True)
        response = urllib2.urlopen(request)
        encoding = response.headers['content-type'].split('charset=')[-1]
        content = response.read().decode(encoding)
        if '登录成功' in content:
            print '登录成功！'
            time_remains = re.findall('套餐剩余.*', content)
            if time_remains:
                print re.sub('<[^<]+?>', '', time_remains[0])
        else:
            print '登录失败！'


def logout(domain, info):
    logout_url = domain.replace('input', 'logout')
    params = urllib.urlencode(info)
    request = urllib2.Request(url=logout_url, data=params, unverifiable=True)
    response = urllib2.urlopen(request)
    if response.code == 200:
        print '成功下线！'


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'login':
            domain, login_info = get_info()
            login(domain, login_info)
        if sys.argv[1] == 'logout':
            with open(info_file, 'r') as f:
                d = json.load(f)
            domain = d['domain']
            logout_info = d['logout_info']
            logout(domain, logout_info)
    else:
        print """Invalid command. Please use
        ``python cmcc.py login`` to login
        ``python cmcc.py logout`` to logout"""
