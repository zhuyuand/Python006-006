#!/bin/python3
# -*- coding: utf-8 -*-
from configparser import ConfigParser
def db_config(filenme='db_config.ini', section='mysql'):
    '''去配置文件'''
    paeser = ConfigParser()
    paeser.read(filenme, encoding='utf-8')
    if paeser.has_section(section):
        data = paeser.items(section)
        return dict(data)
    raise Exception(f'{section} not found in the {filenme} ')
if __name__ == '__main__':
    print(db_config())