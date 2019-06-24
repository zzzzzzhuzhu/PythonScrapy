#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Administrator
# @time : 2019/6/24 11:01
# @File : DoubanBookTOP250.py
"""
豆瓣图书TOP250
"""
from queue import Queue
import requests
import re
from threading import Thread


class MyThtead(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) -> None:
        while True:
            url = self.queue.get()
            try:
                for info in GetRankInfo(url):
                    return info
            finally:
                self.queue.task_done()


def GetRankInfo(url):
    respone = requests.get(url)
    if respone.status_code == 200:
        content = respone.text
        # 正则匹配需要的内容
        result = re.findall('<div class="pl2">.*?<a href="(.*?)".*?title="(.*?)".*?>.*?'
                            '</a>.*?class="star clearfix">.*?class="rating_nums">(.*?)</span>.*?class="pl">[(](.*?)[)]</span>',
                            content, re.S)
        for info in result:
            yield {
                'href': info[0],
                'name': info[1],
                'start': info[2],
                'comment': info[3].replace('\n', '').strip(),
            }


if __name__ == '__main__':
    # 爬取链接集合
    base_url = 'https://book.douban.com/top250?start={}'
    urls = [base_url.format(starts) for starts in range(0, 250, 25)]
    queue = Queue()
    for x in range(10):
        worker = MyThtead(queue)
        worker.daemon = True
        worker.start()
    for url in urls:
        queue.put(url)
    queue.join()
