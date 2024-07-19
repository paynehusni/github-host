#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   liuyuqi.gov@msn.cn
@Time    :   2019/08/03 17:02:15
@License :   Copyright © 2017-2022 liuyuqi. All Rights Reserved.
@Desc    :   get ip from ip address
'''

from email import header
import requests
from bs4 import BeautifulSoup
import re
import json


def getIpFromIpaddress(site):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
        'Host': 'ipaddress.com'
    }
    url = "https://www.ipaddress.com/site/" + site
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()  # 确保我们为错误的状态码引发错误
        
        if res.text.strip() == "":
            raise ValueError("从服务器收到空响应。")
        
        soup = BeautifulSoup(res.text, 'html.parser')
        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", res.text)
        
        if ip:
            trueip = ip[0]  # 返回找到的第一个IP地址
        else:
            raise ValueError("在响应中未找到IP地址。")
    except requests.RequestException as e:
        print(f"查询 {site} 时出错：{e}")
    except ValueError as ve:
        print(f"值错误：{ve}")
    return trueip


def getIpFromChinaz(site):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
               'Host': 'ip.tool.chinaz.com'}
    url = "http://ip.tool.chinaz.com/" + site
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all('span', class_="Whwtdhalf w15-0")
        for c in result:
            ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", c.text)
            if len(ip) != 0:
                trueip = ip[0]
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
    return trueip


def getIpFromWhatismyipaddress(site):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
               'Host': 'ip.tool.chinaz.com'}
    url = "https://whatismyipaddress.com//hostname-ip"
    data = {
        "DOMAINNAME": site,
        "Lookup IP Address": "Lookup IP Address"
    }
    trueip = None
    try:
        res = requests.post(url, headers=headers, data=data, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all('span', class_="Whwtdhalf w15-0")
        for c in result:
            ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", c.text)
            if len(ip) != 0:
                trueip = ip[0]
    except Exception as e:
        print("查询" + site + " 时出现错误: " + str(e))
    return trueip


def getIpFromipapi(site):
    '''
    return trueip: None or ip
    '''
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
               'Host': 'ip-api.com'}
    url = "http://ip-api.com/json/%s?lang=zh-CN" % (site)
    trueip = None
    for i in range(5):
        try:
            res = requests.get(url, headers=headers, timeout=5)
            res = json.loads(res.text)
            if(res["status"] == "success") and len(re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", res["query"])) == 1:
                trueip = res["query"]
                break
        except Exception as e:
            print("查询" + site + " 时出现错误: " + str(e))
    return trueip
