#!/bin/python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser


def db_config(filename='dbconfig.ini', section='mysql'):
    config = ConfigParser()
    config.read(filename)
    if config.has_section(section):
        items = config.items(section)
    else:
        raise Exception(
            '{} has not found in the {} file '.format(
                section, filename))
    return dict(items)


if __name__ == '__main__':
    print(db_config())
