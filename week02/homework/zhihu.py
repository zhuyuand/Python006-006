#!/bin/python3
# -*- coding: utf-8 -*-
'''
你觉得《奇葩说》里面最让你惊艳的观点是什么？
url https://www.zhihu.com/question/270934835/answer/841790498
referer: https://www.zhihu.com/search?type=content&q=%E4%BD%A0%E8%A7%89%E5%BE%97%E3%80%8A%E5%A5%87%E8%91%A9%E8%AF%B4%E3%80%8B%E9%87%8C%E9%9D%A2%E6%9C%80%E8%AE%A9%E4%BD%A0%E6%83%8A%E8%89%B3%E7%9A%84%E8%A7%82%E7%82%B9%E6%98%AF%E4%BB%80%E4%B9%88%EF%BC%9F
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36
https://www.zhihu.com/api/v4/questions/270934835/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics;data[*].settings.table_of_content.enabled&limit=3&offset=3&platform=desktop&sort_by=default
'''
import requests
from urllib.parse import quote
import requests
from fake_useragent import UserAgent
from xml import etree
question = '你觉得《奇葩说》里面最让你惊艳的观点是什么？'
id = 270934835
referer = 'https://www.zhihu.com/search?type=content&q=' + quote(question)
headers = {
    # 'referer': referer,
    'user-agent': UserAgent(verify_ssl=False).random
}


def spider(url):
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    all = res.json()
    print(all)
    totals = all['paging']['totals']
    print(f'一共有{totals}回答')
    data = all['data']
    con_list = []
    for i in data:
        tmp = i['content']
        con_list.append(tmp)
    next_url = all['paging']['next']
    return con_list, totals, next_url


if __name__ == '__main__':
    fp = open('./spider.txt', mode='a+', encoding='utf-8')
    i = 0
    url = f'https://www.zhihu.com/api/v4/questions/{id}/answers?include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,is_recognized;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics;data[*].settings.table_of_content.enabled&limit=3&offset=0&platform=desktop&sort_by=default'
    while i <= 1643:
        con_list, totals, url = spider(url=url)
        fp.write('\r\n'.join(con_list))
        i += 1
    fp.close()
