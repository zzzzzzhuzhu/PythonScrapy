#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Administrator
# @time : 2019/6/24 17:40
# @File : EmojoGet.py 

"""表情包图片爬取"""

import requests
from bs4 import BeautifulSoup

url = 'https://fabiaoqing.com/biaoqing/lists/page/1.html'
respone = requests.get(url)
soup = BeautifulSoup(respone.text, 'lxml')
# todo 表情包爬取待完成
