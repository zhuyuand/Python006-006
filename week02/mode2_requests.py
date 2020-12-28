#!/bin/python3
# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import requests
from requests.exceptions import ConnectTimeout
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {'user-agent': ua}
myurl = 'https://movie.douban.com/top250'
try:
    response = requests.get(url=myurl, headers=header)
except ConnectTimeout as e:
    print(f'超时 {e}')
    sys.exit(1)
p = Path(__file__)
dir = p.resolve().parent
html_path = dir.joinpath('html')
# 判断不存在文件夹（1.是否存在 2.是否为文件夹）
if not html_path.is_dir():
    # 创建文件
    html_path.mkdir()
    # Path.mkdir(html_path)
page = html_path.joinpath('douban.html')
try:
    with open(page, 'w', encoding='utf-8') as f:
        f.write(response.text)
except FileNotFoundError as e:
    print(f'file not found {e}')
except IOError as e:
    print(f'io error {e}')
except Exception as e:
    print(f'{e}')
