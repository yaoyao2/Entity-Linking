#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import sys


NotFindQID=[]
NotFindQNAME=[]
DBIdNameText=''

def edit(str1, str2):
    matrix = [[i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                d = 0
            else:
                d = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    return matrix[len(str1)][len(str2)]



def DBIdName2Text():

    path='DBIdName.txt'
    count=0
    T=open('DBNameText.txt','w',encoding='utf-8')
    with open(path,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        tempText=''
        while line:

            bath=int(count/20000)
            if(bath<=(count/20000)<bath+1):
                if(count%2==0):
                    DBId=line
                if(count%2==1):
                    tempText = tempText +' '+DBId+' '+line.lower()
                    line=line.lower()
                    if(line.find(',')!=-1):
                        name = line.split(',')
                        for n in name:
                            tempText = tempText + ' ' + DBId+' '+n.strip(' ')

            if((20000*(bath+1))==(count+1)):
                T.write(tempText+'\n')
                tempText=''
            if(count==1637481):
                T.write(tempText + '\n')
                tempText = ''

            count = count + 1
            # if(count>2000):
            #     break
            print(count)
            line=f.readline().strip('\n')
    T.close()

    pass



def ReadDBNameText():
    global DBIdNameText

    with open('DBNameText.txt',encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            DBIdNameText=DBIdNameText+' '+line
            line = f.readline().strip('\n')

        pass





def WanQuanYingPiPei(docQueryPath,dbEntityPath):
    ansf=open(dbEntityPath,'w',encoding='utf-8')
    with open(docQueryPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            if(line.find(' NIL')==-1):
                pos=line.find(' E0')
                docId=line.split(' ')[0]
                query=line[len(docId)+1:pos]
                ansId=line[pos+1:pos+9]
                entity=line[pos+10:]
            else:
                pos=line.find(' NIL')
                docId=line.split(' ')[0]
                query=line[len(docId)+1:pos+1]
                end=line.find(' XXX')
                ansId=line[pos+1:end]
                entity=line[pos+ 9:]
            print(docId)
            # print(query)######  mention
            # print(ansId)######  正确答案的id
            # print(entity)#######  answer
            ###############我现在是想non-NIL的候选集找30个，NIL的可以不管
            houxuanId=''
            querypos=DBIdNameText.find(query.lower())
            houCount=0
            while querypos!=-1:

                begpos=DBIdNameText.find('E0',querypos-10)
                endpos=DBIdNameText.find('E0',querypos)
                if(begpos!=-1):
                    findStr=DBIdNameText[begpos:endpos]
                    kuohaoPos=findStr.find('(')
                    # print(findStr)
                    if(kuohaoPos!=-1 and findStr.find(query.lower())<kuohaoPos):
                        #有括号
                        findEntity=findStr[9:kuohaoPos]
                        if(findEntity.strip(' ')==query.strip(' ').lower()):
                            # lower一模一样
                            houxuanId = houxuanId + ' ' + DBIdNameText[begpos:begpos + 8]
                            houCount = houCount + 1
                            print(query+' MMMMM '+findEntity)


                    if(kuohaoPos==-1):
                        #没有括号
                        findEntity=findStr[9:]
                        if (findEntity.strip(' ') == query.strip(' ').lower()):
                            # lower一模一样
                            houxuanId = houxuanId + ' ' + DBIdNameText[begpos:begpos + 8]
                            houCount = houCount + 1
                            print(query + ' MMMMM ' + findEntity)

                        pass


                querypos = DBIdNameText.find(query.lower(),querypos+1)


            if(ansId.find('NIL')==-1):
                if(houxuanId.find(ansId)==-1):
                    #有答案的实体，没有找到答案，就用答案去找答案

                    entitypos = DBIdNameText.find(entity.lower())
                    print("kkkk"+entity.lower())
                    while entitypos != -1:

                        begpos = DBIdNameText.find('E0', entitypos - 10)
                        endpos = DBIdNameText.find('E0', entitypos)
                        if (begpos != -1):
                            findStr = DBIdNameText[begpos:endpos]
                            # print(findStr)
                            # 没有括号
                            findEntity = findStr[9:]
                            if (findEntity.strip(' ') == entity.strip(' ').lower()):
                                # lower一模一样
                                houxuanId = houxuanId + ' ' + DBIdNameText[begpos:begpos + 8]
                                houCount = houCount + 1
                                print(query + ' MMMMM ' + findEntity)

                            pass

                        entitypos = DBIdNameText.find(entity.lower(), entitypos + 1)




            ansf.write(line+'\n')
            ansf.write(ansId.strip(' ')+' '+str(houCount)+' '+houxuanId.strip(' ')+'\n')
            line=f.readline().strip('\n')

    pass




if __name__=='__main__':
    # DBIdName2Text()
    # ReadDBNameText()
    # for i in range(138):
    #     docQueryPath="./docQuery/doc_"+str(i+1)+"_uni.txt"
    #     dbEntityPath="./dbEntity/db_"+str(i+1)+".txt"
    #     WanQuanYingPiPei(docQueryPath,dbEntityPath)


    year='2009'; fileNum=3695
    # year='2010'; fileNum=2231
    # year='2011'; fileNum=2231
    # year='2012'; fileNum=2016
    # year='2013'; fileNum=1820
    # year='2014'; fileNum=138

    ReadDBNameText()
    for i in range(fileNum):
        docQueryPath = u"H:\yaojuan\QUERY\\"+year+"\\eval\\test_docQuery\doc_" + str(i + 1) + "_uni.txt"
        dbEntityPath = u"H:\yaojuan\QUERY\\"+year+"\\eval\\test_dbEntity\db_" + str(i + 1) + ".txt"
        WanQuanYingPiPei(docQueryPath, dbEntityPath)


