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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    url = "https://www.ipaddress.com/site/" + site
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()  # 确保我们为错误的状态码引发错误
        
        # 打印响应状态码和部分响应内容用于调试
        print("响应状态码:", res.status_code)
        print("响应头:", res.headers)
        print("响应内容:", res.text[:1000])  # 打印前1000个字符

        if res.text.strip() == "":
            raise ValueError("从服务器收到空响应。")
        
        soup = BeautifulSoup(res.text, 'html.parser')
        ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", res.text)
        
        if ip:
            trueip = ip[0]  # 返回找到的第一个IP地址
        else:
            raise ValueError("在响应中未找到IP地址。")
    except requests.RequestException as e:
        print(f"查询 {site} 时请求错误：{e}")
        if res is not None:
            print("响应内容:", res.text)
    except ValueError as ve:
        print(f"值错误：{ve}")
    except Exception as e:
        print(f"未知错误：{e}")
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"http://ip-api.com/json/{site}?lang=zh-CN"
    trueip = None

    for i in range(5):
        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()  # 检查是否有HTTP错误
            data = res.json()  # 直接将响应解析为JSON
            print(f"Debug: 响应数据: {data}")  # 打印调试信息
            if data["status"] == "success" and re.match(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", data["query"]):
                trueip = data["query"]
                break
        except requests.RequestException as e:
            print(f"查询 {site} 时出现网络错误: {e}")
        except json.JSONDecodeError:
            print(f"查询 {site} 时返回的不是有效的JSON")
        except KeyError:
            print(f"查询 {site} 时返回的JSON格式不正确: {res.text}")
        except Exception as e:
            print(f"查询 {site} 时出现未知错误: {e}")
    
    return trueip
