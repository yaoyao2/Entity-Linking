#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import sys
allFileNum = 0


def printPath(level, path):
    global allFileNum
    '''''
    打印一个目录下的所有文件夹和文件
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    of = open('DocFileName.txt', 'w')


    for f in files:
        #判断是不是文件夹
        if (os.path.isdir(path + '/' + f)):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if (f[0] == '.'):
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        #判断是不是文件
        if (os.path.isfile(path + '/' + f)):
            # 添加文件
            fileList.append(f)
            doc_id=f
            print(f)
            #将DB的文件名写入‘DBFileName.txt’中
            of.write(f+'\n')






    of.close( )
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        if (i_dl == 0):
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            print('#########' * (int(dirList[0])), dl)

            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)

    for fl in fileList:
        # 打印文件
       # print '-------' * (int(dirList[0])), fl
       # 顺便计算一下有多少个文件
        allFileNum = allFileNum + 1


if __name__=='__main__':
    path=u'H:\\yaojuan\\QUERY\\2014\\eval\\source_documents'
    printPath(1,path)

    pass