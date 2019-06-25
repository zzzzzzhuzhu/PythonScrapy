#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author : Administrator
# @time : 2019/6/24 17:40
# @File : EmojoGet.py

"""
表情包图片爬取
源网址：https://fabiaoqing.com/
"""
from queue import Queue

import requests
from bs4 import BeautifulSoup
import os
from threading import Thread


class EmpjoyThrtead(Thread):

    def __init__(self, queue, path):
        Thread.__init__(self)
        self.queue = queue
        self.path = path

    def run(self) -> None:
        while True:
            url = self.queue.get()
            try:
                print("线程 {} 执行任务，进行爬取".format(Thread.getName(self)))
                GetImg(url, self.path)
            finally:
                self.queue.task_done()


def GetImg(url, path):
    respone = requests.get(url)
    if respone.status_code == 200:
        soup = BeautifulSoup(respone.text, 'lxml')
        imgblock = soup.find_all('img', class_='ui image lazy')
        for imgtag in imgblock:
            img_url = imgtag.get('data-original')
            img_name = (img_url.split('/')[-1]).split('.')[0]
            img_type = os.path.splitext(img_url)[-1]
            savepath = os.path.join(path, (img_name + img_type))
            imgrespone = requests.get(img_url)
            if imgrespone.status_code == 200:
                # 保存图片
                with open(savepath, 'wb') as files:
                    files.write(imgrespone.content)
    else:
        respone.raise_for_status()


if __name__ == '__main__':
    if not os.path.exists('EmojoFile'):
        os.mkdir('EmojoFile')
    emjopath = (os.path.abspath('EmojoFile'))
    # 爬取链接
    url = 'https://fabiaoqing.com/biaoqing/lists/page/{}.html'
    url_list = [url.format(i) for i in range(1, 201)]
    queue = Queue()
    for x in range(10):
        worker = EmpjoyThrtead(queue, emjopath)
        worker.daemon = True
        worker.start()
    for url in url_list:
        queue.put(url)
    queue.join()
    print("退出主线程")
