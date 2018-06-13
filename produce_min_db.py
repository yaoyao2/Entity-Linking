#!/usr/bin/python
# -*- coding:utf8 -*-

from data_handle import doc_query

Map=dict()
AnsIdSet=set()
StoreTempSet=set()

def ReadDBIndex(indexPath):
    global Map
    with open(indexPath,encoding='utf-8') as f:
        line=f.readline().strip('\n').strip(' ')
        while line:
            L=line.split(' ')
            Map[L[0]]=line
            line=f.readline().strip('\n').strip(' ')
    return Map



def ReadAnswer(answerPath):
    global AnsIdSet
    lineCount=0
    with open(answerPath,encoding='utf-8') as f:
        line=f.readline().strip('\n').strip(' ')
        while line:
            if(lineCount%2==0):
                pass
            if(lineCount%2==1):
                line=line.split(' ')
                for i in range(len(line)-2):
                    if(len(line[i+2])>2):
                        # print(line[i+2])
                        AnsIdSet.add(line[i+2])
            lineCount=lineCount+1
            line=f.readline().strip('\n').strip(' ')
    return AnsIdSet



def ProduceMinDB(dbTextPath,year):
    global StoreTempSet
    f=open(u'H:\yaojuan\QUERY\\'+year+'\\eval\\test_minDB.txt','w',encoding='utf-8')
    for key in Map:
        if(key in AnsIdSet):
            line=Map[key].split(' ')
            for i in line:
                if(i not in AnsIdSet):
                    AnsIdSet.add(i)
                    StoreTempSet.add(i)

    tempF=open('Temp.txt','w',encoding='utf-8')
    while len(StoreTempSet)!=1:
        ###E0006472没有
        print(len(StoreTempSet))
        print(StoreTempSet)
        for key in Map:
            if(key in StoreTempSet):
                StoreTempSet.remove(key)
                line=Map[key].split(' ')
                for i in line:
                    if(i not in AnsIdSet):

                        tempF.write(i+'\n')

                        AnsIdSet.add(i)
                        StoreTempSet.add(i)

    IdNameMap = doc_query.readIdNameFile(dbIdNamePath=u'DBIdName.txt')
    tempCount=0
    AnsIdSet.remove('E0006472')

    for i in AnsIdSet:
        print(len(AnsIdSet))
        if(i.find('E0')==-1):
            print(i)

        else:
            tempCount=tempCount+1

            f.write(i+'\n')
            f.write(IdNameMap[i]+'\n')
            num=IdNameMap[i].split('###')[0]
            dbPath = dbTextPath + num +'.txt'
            print(dbPath)
            textf = open(u'H:\yaojuan\QUERY\\'+year+'\\eval\\test_minDBText\dbText_' + str(tempCount) + '.txt', 'w', encoding='utf-8')
            with open(dbPath,encoding='utf-8') as dbf:
                line=dbf.readline()
                while line:
                    textf.write(line)
                    if(line.find('</facts>')!=-1):
                        break
                    line=dbf.readline()
            dbf.close()
            textf.close()


    return AnsIdSet




if __name__=='__main__':
    # year='2009'
    # filesnum=3695

    year='2010'
    filesnum=2231

    # year='2011'
    # filesnum=2231

    # year = '2012'
    # filesnum = 2016

    # year='2013'
    # filesnum=1820

    # year='2014'
    # filesnum=138


    indexPath = u'DB_id_index.txt'
    ReadDBIndex(indexPath)
    for i in range(filesnum):#文件个数
        answerPath = u'H:\yaojuan\QUERY\\'+year+'\\eval\\test_dbEntity\db_' + str(i + 1) + '.txt'
        ReadAnswer(answerPath)
    dbTextPath = u'H:\\yaojuan\\EntityLinkingData\\data\\'
    ProduceMinDB(dbTextPath,year)



    pass






