#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import sys

def handleDBIdName(path):

    with open(path,encoding='utf-8') as f:
        line=f.readline().strip('\n')

        while line:
            print(line)
            if(line.find('(')):
                pass



            line = f.readline().strip('\n')


    pass




if __name__=='__main__':
    path='DBIdName.txt'
    handleDBIdName(path)

    pass