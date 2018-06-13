#!/usr/bin/python
# -*- coding:utf8 -*-

import jieba
import nltk
from bs4 import BeautifulSoup
from data_handle import doc_query
wordVecIndexMap=dict()

def Score():
    pass

# def readWordVecIndex():
#     global wordVecIndexMap
#     path=u'E:\mypython_Linking\CNN\glove.6B.100d.txt'
#     #path = u'E:\data_analysis\word2vec\\vector_100.txt'
#     count=0
#     with open(path,encoding='utf-8') as f:
#         line=f.readline()
#         while line:
#             count=count+1
#             wordVecIndexMap[line.split(' ')[0]]=count
#             line=f.readline()
#
#     return wordVecIndexMap


def NewText(word_tag):

    String=''
    for i in word_tag:

        word=i[0]
        tag=i[1]
        # if(tag.find('N')!=-1):
        #     print(i)
        ###去掉一些消歧无意义的单词
        #去掉CD、PRP、VBD、CC、WDT,IN,RP,TO,DT
        not_hold=['CD']
        if tag not in not_hold:
            if(len(word)>1):
                String=String+word+' '

    return String



def FindRelation(mindbPath,newMinDBTextPath,relation,mindbIndex,mindbAllIndex):

    newf=open(newMinDBTextPath,'w',encoding='utf-8')
    dbText=''
    attributeText=''
    entityName=''
    entityId=''
    with open(mindbPath, encoding='utf-8') as f:
        line=f.readline()
        while line:
            # print(line)
            if(line.find('<entity id=')!=-1):
                pos1=line.find('name="')
                pos2=line.find('"',pos1+7)
                entityName=line[pos1+6:pos2]

                pos3=line.find('id="')
                pos4=line.find('"',pos3+5)
                entityId=line[pos3+4:pos4]

                # print("entityName:"+entityName)
                # print("entityId:"+entityId)

            if(line.find('<fact ')!=-1):
                pos1=line.find('name="')
                pos2=line.find('"',pos1+7)
                rel=line[pos1+6:pos2]
                # print("rel:"+rel)
                # relation.write(rel+'\n')

                pass

            dbText=dbText+line
            if(line.find('id="E')==-1):
                attributeText=attributeText+line
            line=f.readline()
            pass
    soup = BeautifulSoup(dbText, 'html.parser')
    newText = doc_query.preprocessor(soup.get_text())
    words = nltk.word_tokenize(newText)
    word_tag = nltk.pos_tag(words)
    newText = NewText(word_tag)
    # print(newText)
    newf.write(newText+'\n')


    entity = doc_query.preprocessor(entityName)
    entityIndex = doc_query.getWordIndex(entity)
    textIndex = doc_query.getWordIndex(newText)
    newf.write(entityIndex+'\n')
    newf.write(textIndex+'\n')
    ####想要的文件1 db所有上下文
    mindbAllIndex.write(entityId+' '+entityIndex+' '+textIndex+'\n')
    mindbAllIndex.write(entityId+' '+entityIndex+'\n')

    fre = doc_query.DocWordfrequency(newText)
    for w in fre:
        newf.write(w.strip(' ') + '\n')

    newf.close()

    #########################################################
    soup = BeautifulSoup(attributeText, 'html.parser')
    newText = doc_query.preprocessor(soup.get_text())
    words = nltk.word_tokenize(newText)
    word_tag = nltk.pos_tag(words)
    newText = NewText(word_tag)
    textIndex = doc_query.getWordIndex(newText)
    ####想要的文件2 db所有属性
    mindbIndex.write(entityId + ' ' + entityIndex+' '+textIndex + '\n')
    mindbIndex.write(entityId + ' ' + entityIndex + '\n')
    print(textIndex)
    # print(len(textIndex.split(' ')))
    # print(len(textIndex.split(' ')))
    # print(len(textIndex.split(' ')))
    # print(len(textIndex.split(' ')))
    # if(len(textIndex.split(' '))==0):
    #     print("KKKKKKKKKK!!!")




    pass




if __name__=='__main__':

    # year='2009'; dbnum=106783; testFlage=True

    # year='2009'; dbnum=123710; testFlage=True
    year='2010'; dbnum=140097; testFlage=True   #126840

    # year='2010'; dbnum=121050; testFlage=True     ##train dbnum=123129

    # year='2010'; dbnum=123129; testFlage=False  ##train train train

    # year='2011'; dbnum=118890; testFlage=True

    # year='2012'; dbnum = 113069; testFlage=True

    # year='2013'; dbnum=140190; testFlage=True

    # year='2014'; dbnum=142416; testFlage=True     ##train dbnum=144346

    # year='2014'; dbnum=144346; testFlage=False  ##train train train

    if(testFlage):
        doc_query.readWordVecIndex()
        relation = open("relation.txt", 'w', encoding='utf-8')
        mindbIndex = open(u'H:\yaojuan\QUERY\\'+year+'\\eval\word2vec\\test_mindbIndex.txt','w',encoding='utf-8')
        mindbAllIndex = open(u'H:\yaojuan\QUERY\\'+year+'\\eval\word2vec\\test_mindbAllIndex.txt','w',encoding='utf-8')

        for i in range(dbnum):#113069
            mindbPath=u'H:\yaojuan\QUERY\\'+year+'\\eval\\test_minDBText\dbText_'+str(i+1)+'.txt'
            newMinDBTextPath=u'H:\yaojuan\QUERY\\'+year+'\\eval\word2vec\\test_minDBTextOnly\dbText_'+str(i+1)+'.txt'
            FindRelation(mindbPath,newMinDBTextPath,relation,mindbIndex,mindbAllIndex)

        # relation.close()
        mindbIndex.close()
        mindbAllIndex.close()
    else:
        doc_query.readWordVecIndex()
        relation = open("relation.txt", 'w', encoding='utf-8')
        mindbIndex = open(u'H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train_mindbIndex.txt', 'w', encoding='utf-8')
        mindbAllIndex = open(u'H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train_mindbAllIndex.txt', 'w', encoding='utf-8')

        for i in range(dbnum):  # 113069
            mindbPath = u'H:\yaojuan\QUERY\\' + year + '\\training\\train_minDBText\dbText_' + str(i + 1) + '.txt'
            newMinDBTextPath = u'H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train_minDBTextOnly\dbText_' + str(i + 1) + '.txt'
            FindRelation(mindbPath, newMinDBTextPath, relation, mindbIndex, mindbAllIndex)

        # relation.close()
        mindbIndex.close()
        mindbAllIndex.close()
    pass
























