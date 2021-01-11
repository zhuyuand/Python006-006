#!/bin/python3
# -*- coding: utf-8 -*-
import enum


class Gender(enum.Enum):
    male = 0
    woman = 1

class Edu(enum.Enum):
    undergraduate = '本科'
    master = '硕士'
    doctor = '博士'
if __name__ == '__main__':
    print(Gender.male.value)