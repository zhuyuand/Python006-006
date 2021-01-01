#!/bin/python3
# -*- coding: utf-8 -*-
from  fake_useragent import UserAgent
import requests
# 减少爬虫频率
import time
# 解析html
from lxml import etree
def get_url_name(url:str):
    '''获取电影名称和链接'''
    headers = {
        'user-agent': UserAgent(verify_ssl=False).random
    }
    res = requests.get(url, headers=headers)
    selectors = etree.HTML(res.text)
    names = selectors.xpath('//div[@class="hd"]/a/span[1]/text()')
    links = selectors.xpath('//div[@class="hd"]/a/@href')
    info = dict(zip(names, links))
    for i in info:
        print(f'电影名称 {i}\t\t链接 {info[i]}')
if __name__ == '__main__':

    URLS = tuple(f'https://movie.douban.com/top250?start={ page * 25 }&filter=' for page in range(10))
    for url in URLS:
        get_url_name(url)
        time.sleep(5)
