#!/usr/bin/python
# -*- coding:utf8 -*-

#
# ansf=open('all.txt','w',encoding='utf-8')
import random

count1=0
uniMap=dict()

def handleTrainDBEntity(dbPath,queryPath,newf,allF):

    Map=dict()
    with open(dbPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        lineCount=0
        while line:
            if(lineCount%2==0):
                subStr=line[len(line.split(' ')[0]):]
                # print(subStr)
            if(lineCount%2==1):
                ans=line
                Map[subStr]=line
                pass
            lineCount=lineCount+1
            line=f.readline().strip('\n')

    with open(queryPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            lineCount=lineCount+1
            subStr=line[len(line.split(' ')[0]+' '+line.split(' ')[1]):line.find(' beg=')]
            # print(dbPath)
            # print(subStr)
            # print(line)
            # print(Map[subStr])
            newf.write(line+'\n')
            newf.write(Map[subStr]+'\n')
            queryId=line.split(' ')[1]
            templine=Map[subStr].split(' ')
            ansId=templine[0]
            ansNum=templine[1]
            if(subStr.find('XXXXX')==-1):
                # if(len(templine)-2==1):
                #     print(subStr)
                flag=True
                for i in range(len(templine)-2):
                    houId=templine[i+2]
                    if(len(houId.strip(' '))>0):
                        if(ansId==houId):
                            tempStr=queryId+' '+houId+' '+'1'
                            allF.write(tempStr+'\n')
                        elif(ansId!=houId and flag):
                            tempStr=queryId+' '+houId+' '+'0'
                            allF.write(tempStr+'\n')
                            flag=False

            line=f.readline().strip('\n')
    newf.close()

    pass




def handleDBEntity(dbPath,queryPath,newf,allF):
    global count1
    global uniMap
    map=dict()
    Map=dict()
    with open(dbPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        lineCount=0
        while line:
            if(lineCount%2==0):
                subStr=line[len(line.split(' ')[0]):]
                # print(subStr)
            if(lineCount%2==1):
                ans=line
                Map[subStr]=line
                pass
            lineCount=lineCount+1
            line=f.readline().strip('\n')
    with open(queryPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')

        while line:
            lineCount=lineCount+1
            subStr=line[len(line.split(' ')[0]+' '+line.split(' ')[1]):line.find(' beg=')]
            print(line)
            print(dbPath)
            print(subStr)
            print(line)
            print(Map[subStr])
            newf.write(line+'\n')
            newf.write(Map[subStr]+'\n')
            queryId=line.split(' ')[1]
            templine=Map[subStr].split(' ')
            # ansId=templine[0]
            # ansNum=templine[1]
            # print(ansId)
            for i in range(len(templine)):
                if(i==0):
                    ansId=templine[0]
                if(i==1):
                    ansNum=int(templine[1])
                if(i>1 and ansNum>0):
                    houId=templine[i]
                    if(len(houId.strip(' '))>0):
                        if(ansId==houId):
                            tempStr=queryId+' '+houId+' '+'1'
                            if tempStr not in uniMap:
                                uniMap[tempStr]=1
                            else:
                                uniMap[tempStr]=uniMap[tempStr]+1
                            count1=count1+1
                            allF.write(tempStr+'\n')
                        else:
                            if(ansId.find('E0')!=-1):
                                if ansId not in map:
                                    map[ansId]=1
                                    print(ansId)
                            tempStr=queryId+' '+houId+' '+'0'
                            allF.write(tempStr+'\n')
                            # if(ansId.find('NIL')==-1):
                            #     tempStr=queryId+' '+ansId+' '+'1'
                            #     allF.write(tempStr + '\n')
                            # break

            line=f.readline().strip('\n')
    newf.close()


    pass



if __name__=='__main__':

    # allF=open('H:\yaojuan\QUERY\\2010\\training\\train_all_data.txt','w',encoding='utf-8')
    # for i in range(1453):
    #
    #     dbPath='H:\yaojuan\QUERY\\2010\\training\\train_dbEntity\db_'+str(i+1)+'.txt'
    #     queryPath='H:\yaojuan\QUERY\\2010\\training\\train_docQuery\doc_'+str(i+1)+'.txt'
    #     newdbPath='H:\yaojuan\QUERY\\2010\\training\\train_dbEntity\db_'+str(i+1)+'_new.txt'
    #     newf=open(newdbPath,'w',encoding='utf-8')
    #     handleDBEntity(dbPath,queryPath,newf,allF)
    #
    # allF.close()
    # print(len(uniMap))
    # print(count1)

    year='2009'; fileNum=3695
    # year='2010';fileNum=2231
    # year='2011'; fileNum=2231
    # year='2012'; fileNum=2016
    # year='2013'; fileNum=1820
    # year='2014'; fileNum=138


    # allF = open('H:\yaojuan\QUERY\\'+year+'\\eval\\test_all_data.txt', 'w', encoding='utf-8')
    allF = open("H:\yaojuan\QUERY\\"+year+"\eval\word2vec\\test_all_data.txt', 'w', encoding='utf-8")

    for i in range(fileNum):
        dbPath = 'H:\yaojuan\QUERY\\'+year+'\\eval\\test_dbEntity\db_' + str(i + 1) + '.txt'
        queryPath = 'H:\yaojuan\QUERY\\'+year+'\\eval\\test_docQuery\doc_' + str(i + 1) + '.txt'
        newdbPath = 'H:\yaojuan\QUERY\\'+year+'\\eval\\test_dbEntity\db_' + str(i + 1) + '_new.txt'
        newf = open(newdbPath, 'w', encoding='utf-8')
        handleDBEntity(dbPath, queryPath, newf, allF)

    allF.close()
    print(len(uniMap))
    print(count1)




    # allF = open('train_all_data.txt', 'w', encoding='utf-8')
    # for i in range(138):
    #     dbPath = 'E:\mypython_Linking\data_handle\\train_dbEntity\db_' + str(i + 1) + '.txt'
    #     queryPath = 'E:\mypython_Linking\data_handle\\train_docQuery\doc_' + str(i + 1) + '.txt'
    #     newdbPath = 'E:\mypython_linking\data_handle\\train_dbEntity\db_' + str(i + 1) + '_new.txt'
    #     newf = open(newdbPath, 'w', encoding='utf-8')
    #     handleTrainDBEntity(dbPath, queryPath, newf, allF)
    #
    # allF.close()
    # pass


















