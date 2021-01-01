#!/bin/python3
# -*- coding: utf-8 -*-
'''
多线程爬知乎
'''
import requests
from threading import Thread
from queue import Queue
import time
from random import randint
from fake_useragent import UserAgent


def total(url):
    res = requests.get(url=url, headers={
        'user-agent': UserAgent(verify_ssl=False).random
    })
    res.encoding = 'utf-8'
    all = res.json()
    print(all)
    return all['paging']['totals']


class CrawlThread(Thread):
    '''把所有url放入队列中'''

    def __init__(self, thread_id):
        super().__init__()
        self.thread_id = thread_id

    def run(self) -> None:
        print(f'线程 {self.thread_id} 开始')
        self.modulator()
        print(f'线程 {self.thread_id} 结束')

    def modulator(self):
        while not q1.empty():
            time.sleep(randint(1, 5))
            index = q1.get()
            url = f'https://www.zhihu.com/api/v4/questions/270934835/answers?data%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics=&data%5B%2A%5D.mark_infos%5B%2A%5D.url=&data%5B%2A%5D.settings.table_of_content.enabled=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized&limit=3&offset={index}&platform=desktop&sort_by=default'
            try:
                res = requests.get(url, headers={
                    'user-agent': UserAgent(verify_ssl=False).random
                })
                res.encoding = 'utf-8'
                q2.put(res.json())
            except Exception:
                pass


class ParserThread(Thread):
    '''解析并放入txt'''

    def __init__(self, thread_id, fp):
        super().__init__()
        self.thread_id = thread_id
        self.fp = fp

    def run(self) -> None:
        print(f'线程 {self.thread_id} 开始')
        # flag标志q1队列全部解决， q2为空
        while flag or q2.qsize() > 0:
            try:
                data = q2.get_nowait()
                self.parser(data)
            except Exception:
                pass
        print(f'线程 {self.thread_id} 结束')

    def parser(self, data):
        try:
            data = data['data']
            con_list = []
            for i in data:
                tmp = i['content']
                con_list.append(tmp)
            self.fp.write('\r\n'.join(con_list))
        except KeyError as e:
            print(e)


if __name__ == '__main__':
    flag = True
    url = 'https://www.zhihu.com/api/v4/questions/270934835/answers?data%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics=&data%5B%2A%5D.mark_infos%5B%2A%5D.url=&data%5B%2A%5D.settings.table_of_content.enabled=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized&limit=3&offset=0&platform=desktop&sort_by=default'
    # 求出一共多少个回答
    tot = total(url)
    q1 = Queue(tot)
    for i in range(tot):
        q1.put(i)
    # 每一页有三个回答
    q2 = Queue(tot)
    crawl = ['crawl_1', 'crawl_2', 'crawl_3', 'crawl_4']
    parser = ['parser_1', 'parser_2', 'parser_3', 'parser_4']
    crawl_list = []
    parser_list = []
    for i in crawl:
        crawl_thread = CrawlThread(i)
        crawl_thread.start()
        crawl_list.append(crawl_thread)
    with open('spider_1.txt', 'a+', encoding='utf-8') as fp:
        for i in parser:
            parser_thread = ParserThread(i, fp)
            parser_thread.start()
            parser_list.append(parser_thread)
        for i in crawl_list:
            i.join()
        flag = False
        for i in parser_list:
            i.join()
    print('主线程结束')
