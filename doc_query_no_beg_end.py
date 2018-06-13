#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import sys
import jieba
import nltk
from bs4 import BeautifulSoup
import re
query_id_list=[]
query_name_list=[]
doc_id_list=[]

answer_query_id_list=[]
answer_query_name_list=[]
answer_query_name_list=[]
answer_db_id_list=[]
answer_db_name_list=[]

db_id_list=[]
db_name_list=[]
wordVecIndexMap=dict()

def readWordVecIndex():
    global wordVecIndexMap
    # path=u'E:\mypython_Linking\CNN\glove.6B.100d.txt'
    path = u'E:\data_analysis\word2vec\\vector_100.txt'
    count=0
    with open(path,encoding='utf-8') as f:
        line=f.readline()
        while line:
            count=count+1
            wordVecIndexMap[line.split(' ')[0]]=count
            line=f.readline()

    return wordVecIndexMap


def preprocessor(text):
    text = re.sub('<[^>]*>','',text)
    emoticons = re.findall('(?::|;|=)(?:\)|\(|D|P)',text)
    text = re.sub('[\W]+',' ',text.lower())+''.join(emoticons).replace('-','')
    return text.strip(' ')


def WordTokener( sent):  # 将单句字符串分割成词
    result = ''
    wordsInStr = nltk.word_tokenize(sent)
    return wordsInStr


def RemoveStopWords(sent):
    stopwords = {}.fromkeys([line.rstrip() for line in open('stopwords.txt',encoding='utf-8')])
    segs = jieba.cut(sent, cut_all=False)
    final = ''
    for seg in segs:
        if seg not in stopwords:
            final += seg
    return final


def DocWordfrequency(doc):
    words = doc.strip('\n').split(' ')
    word_count = {}
    word_list=[]

    for w in words:
        if w in word_count:
            word_count[w] += 1
        else:
            word_count[w] = 1


    for w in sorted(zip(word_count.values(), word_count.keys()), reverse=True):  # 安装词频排序
        # print(w)
        if(len(w[1].strip(' '))>0):
            wStr=w[1]+' '+str(w[0])
            word_list.append(wStr)

    return word_list


def NewText(word_tag):

    String=''
    for i in word_tag:

        word=i[0]
        tag=i[1]
        # if(tag.find('N')!=-1):
        #     print(i)
        ###去掉一些消歧无意义的单词
        #去掉CD、PRP、VBD、CC、WDT,IN,RP,TO,DT
        hold=['NN','NNS','NNP']
        if tag in hold:
            String=String+word+' '

    return String


def getContentIndex(currentText,currentQuery,docIndex,doc_id):
    print("currentText:"+currentText)
    print("currentQuery:"+currentQuery)

    if (currentText.find(currentQuery) != -1):
        pos=currentText.find(currentQuery)
        CurText = preprocessor(currentText[:pos+len(currentQuery)])
        print('CurText='+CurText)
        CurQuery = preprocessor(currentQuery)
        print('****'+currentText)
        print('****'+currentQuery)


        if (CurText.find(CurQuery) != -1):
            pos_beg=CurText.rfind(CurQuery)

            print('####'+CurText[pos_beg:pos_beg+len(CurQuery)])
            print('####'+CurQuery)

            CurText = CurText[:pos_beg + len(CurQuery)]
            textSplit = CurText.split(' ')
            querySplit = CurQuery.split(' ')
            index_beg = len(textSplit)-1 - len(querySplit)
            index_end = len(textSplit)-1
            print("index_beg="+str(index_beg))
            print("index_end="+str(index_end))
            print(textSplit[index_beg:index_end])
            # print(CurQuery)
            # print(textSplit[index_beg:index_end])

            curTextIndex = getWordIndex(CurText)
            curQueryIndex = getWordIndex(CurQuery)
            if (curTextIndex.find(curQueryIndex) != -1):

                contentIndex = ''
                for i in range(index_beg - 10, index_beg):
                    if (i < 0):
                        contentIndex = contentIndex + '0' + ' '
                    else:
                        contentIndex = contentIndex + docIndex[i] + ' '

                for i in range(index_end + 1, index_end + 11):
                    if (i >= len(docIndex)):
                        contentIndex = contentIndex + '0' + ' '
                    else:
                        contentIndex = contentIndex + docIndex[i] + ' '

                print(docIndex[index_beg-1:index_end])
                entityIndex=''
                for i in range(index_beg,index_end):
                    entityIndex=entityIndex+docIndex[i]+' '
                print('entityIndex:'+entityIndex)
                print(doc_id)
                print('contentIndex:' + contentIndex)
            else:
                print("转换成索引后，找不到了！！！！！")

        else:
            print("找不到了！！！！！")

    else:
        print(doc_id)
        print(currentText[-(len(currentQuery) + 2):])
        print(currentQuery)
        print("转化后找不到了！！！！")


    return entityIndex,contentIndex,index_beg,index_end


def getContentNounIndex(currentText,currentQuery,docIndex,doc_id):
    print("currentText:"+currentText)
    print("currentQuery:"+currentQuery)

    if (currentText.find(currentQuery) != -1):
        pos=currentText.find(currentQuery)
        CurText = preprocessor(currentText[:pos+len(currentQuery)])
        CurQuery = preprocessor(currentQuery)
        qian_currentText=currentText[:pos+len(currentQuery)]
        hou_halfText=currentText[pos+len(currentQuery):]
        print('****'+currentText)
        print('****'+currentQuery)


        if (CurText.find(CurQuery) != -1):
            pos_beg=CurText.rfind(CurQuery)

            print('####'+CurText[pos_beg:pos_beg+len(CurQuery)])
            print('####'+CurQuery)

            CurText = CurText[:pos_beg + len(CurQuery)]
            textSplit = CurText.split(' ')
            querySplit = CurQuery.split(' ')
            index_beg = len(textSplit)-1 - len(querySplit)
            index_end = len(textSplit)-1
            print("index_beg="+str(index_beg))
            print("index_end="+str(index_end))
            print(textSplit[index_beg:index_end])
            # print(CurQuery)
            # print(textSplit[index_beg:index_end])

            curTextIndex = getWordIndex(CurText)
            curQueryIndex = getWordIndex(CurQuery)
            if (curTextIndex.find(curQueryIndex) != -1):

                contentIndex = ''

                soup1 = BeautifulSoup(qian_currentText, 'html.parser')
                words1 = nltk.word_tokenize(soup1.get_text())
                word_tag1 = nltk.pos_tag(words1)
                newText1 = NewText(word_tag1)
                textIndex1 = getWordIndex(newText1).strip(' ')
                textIndex1 = '0 0 0 0 0 0 0 0 0 0 ' + textIndex1
                print('textIndex1:' + textIndex1)
                Index1 = textIndex1.split(' ')[-10:]
                print(Index1)

                soup2 = BeautifulSoup(hou_halfText, 'html.parser')
                words2 = nltk.word_tokenize(soup2.get_text())
                word_tag2 = nltk.pos_tag(words2)
                newText2 = NewText(word_tag2)
                textIndex2 = getWordIndex(newText2).strip(' ')
                print('textIndex2:' + textIndex2)
                textIndex2 = textIndex2 + ' 0 0 0 0 0 0 0 0 0 0'
                Index2 = textIndex2.split(' ')[:10]
                print(Index2)

                for i in Index1:
                    contentIndex = contentIndex + ' ' + i
                for j in Index2:
                    contentIndex = contentIndex + ' ' + j

                contentIndex = contentIndex.strip(' ')
                print("find noun index:" + contentIndex)


                print(docIndex[index_beg-1:index_end])
                entityIndex=''
                for i in range(index_beg,index_end):
                    entityIndex=entityIndex+docIndex[i]+' '
                print('entityIndex:'+entityIndex)
                print(doc_id)
                print('contentIndex:' + contentIndex)
            else:
                print("转换成索引后，找不到了！！！！！")

        else:
            print("找不到了！！！！！")

    else:
        print(doc_id)
        print(currentText[-(len(currentQuery) + 2):])
        print(currentQuery)
        print("转化后找不到了！！！！")


    return contentIndex,entityIndex,index_beg,index_end









def readIdNameFile(dbIdNamePath):
    global db_id_list
    global db_name_list
    IdNameMap=dict()
    tempId=''
    tempName=''
    count=0
    with open(dbIdNamePath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:

            if(count%2==0):
                db_id_list.append(line)
                tempId=line
                # print(line)
            if(count%2==1):
                db_name_list.append(line)
                tempName=line
                IdNameMap[tempId]=str(int((count+1)/2))+'###'+tempName

            count=count+1
            line=f.readline().strip('\n')
    return IdNameMap

    pass

def getWordIndex(docText):
    docIndex = ''
    for i in (preprocessor(docText).strip(' ').split(' ')):
        if (i in wordVecIndexMap):
            docIndex = docIndex + str(wordVecIndexMap[i]) + ' '
        else:
            docIndex = docIndex + '0' + ' '

    return docIndex.strip(' ')


def readQueryFile(path):
    global query_id_list
    global query_name_list
    global doc_id_list


    with open(path,encoding='utf-8') as f:
        line=f.readline()

        while line:
            if(line.find('<query id="')!=-1):
                pos1=line.find('<query id=')
                pos2=line.find('">')
                id=line[pos1+11:pos2]
                query_id_list.append(id)
                # print(id)
            if(line.find('<name>')!=-1):
                pos1=line.find('<name>')
                pos2=line.find('</name>')
                name=line[pos1+6:pos2]
                query_name_list.append(name.strip(' '))
                # print(name)
            if(line.find('<docid>')!=-1):
                pos1 = line.find('<docid>')
                pos2 = line.find('</docid>')
                doc = line[pos1+7:pos2]
                doc_id_list.append(doc)
                # print(doc)

            line=f.readline()

    pass


def readAnswerFile(answerPath):
    global answer_query_id_list
    global answer_query_name_list
    global answer_db_id_list
    global answer_db_name_list

    with open(answerPath, encoding='utf-8') as ansf:
        ans_line = ansf.readline().strip('\n')
        while ans_line:
            pos1 = ans_line.find("query_id=")
            pos2 = ans_line.find("query_name=")
            pos3 = ans_line.find("db_id=")
            pos4 = ans_line.find("db_name=")
            query_id = ans_line[pos1 + 9:pos2].strip(' ')
            query_name = ans_line[pos2 + 11:pos3].strip(' ')
            db_id = ans_line[pos3 + 6:pos4].strip(' ')
            db_name = ans_line[pos4 + 8:len(ans_line)].strip(' ')

            # print(query_id)
            # print(query_name)
            # print(db_id)
            # print(db_name)
            answer_query_id_list.append(query_id)
            answer_query_name_list.append(query_name)
            answer_db_id_list.append(db_id)
            answer_db_name_list.append(db_name)

            ans_line = ansf.readline().strip('\n')
            pass

    pass





def findDocQueryAndDbAnswer(docPath,year,testFlag):
    if(testFlag):
        docP=u'H:\yaojuan\QUERY\\'+year+'\\eval\\source_documents'
    else:
        docP=u'H:\yaojuan\QUERY\\'+year+'\\training\\source_documents'

    # OOOMap={}
    # # 检查一下query的答案是不都有链接的实体
    # path = u'H:\\yaojuan\\EntityLinkingData\\DB_id_index.txt'
    # count = 0
    # all = 0
    # with open(path,encoding='utf-8') as f:
    #     line = f.readline()
    #     while line:
    #         all = all + 1
    #         if (len(line) < 12):
    #             count = count + 1
    #             OOOMap[line.split(' ')[0]]="糟糕！！！有答案实体与任何实体没有关系"
    #         else:
    #             OOOMap[line.split(' ')[0]]="OK!!!!没问题"
    #
    #         line = f.readline()
    if(testFlag):
        queryIndexFile = open('H:\yaojuan\QUERY\\'+year+'\\eval\word2vec\\test\\test_queryIndex.txt','w',encoding='utf-8')
        queryNounIndexFile = open('H:\yaojuan\QUERY\\' + year + '\eval\word2vec\\test\\test_queryNounIndex.txt', 'w', encoding='utf-8')
        queryTextIndexFile = open('H:\yaojuan\QUERY\\' + year + '\\eval\word2vec\\test\\test_queryTextIndex.txt', 'w', encoding='utf-8')
    else:
        queryIndexFile = open('H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train\\train_queryIndex.txt', 'w', encoding='utf-8')
        queryNounIndexFile = open('H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train\\train_queryNounIndex.txt', 'w', encoding='utf-8')
        queryTextIndexFile = open('H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train\\train_queryTextIndex.txt', 'w',encoding='utf-8')

    with open(docPath,encoding='utf-8') as docF:
        doc_line=docF.readline()
        doc_count=0

        while doc_line:

            pos=doc_line.find(".xml")
            doc_id=doc_line[:pos]
            doc_count=doc_count+1
            # print(doc_id)


            if(doc_count>0):
                if(testFlag):
                    docfile= open('H:\yaojuan\QUERY\\'+year+'\\eval\word2vec\\test_docQuery\doc_'+str(doc_count)+'.txt','w',encoding='utf-8')
                    unidocfile = open('H:\yaojuan\QUERY\\'+year+'\\eval\word2vec\\test_docQuery\doc_' + str(doc_count) + '_uni.txt', 'w',encoding='utf-8')
                    docindexfile = open('H:\yaojuan\QUERY\\'+year+'\\eval\word2vec\\test_docQuery\doc_' + str(doc_count) + '_Windex.txt', 'w', encoding='utf-8')
                    textfile=open('H:\yaojuan\QUERY\\'+year+'\\eval\word2vec\\test_docText\\text_'+str(doc_count)+'.txt','w',encoding='utf-8')
                else:
                    docfile = open('H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train_docQuery\doc_' + str(doc_count) + '.txt', 'w', encoding='utf-8')
                    unidocfile = open('H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train_docQuery\doc_' + str(doc_count) + '_uni.txt', 'w', encoding='utf-8')
                    docindexfile = open('H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train_docQuery\doc_' + str(doc_count) + '_Windex.txt', 'w', encoding='utf-8')
                    textfile = open('H:\yaojuan\QUERY\\' + year + '\\training\word2vec\\train_docText\\text_' + str(doc_count) + '.txt', 'w', encoding='utf-8')

                with open(docP + "\\" + doc_id+'.xml' , encoding='utf-8') as textF:
                    docText = textF.read()
                DocText=preprocessor(docText.replace('\n',' '))###预处理后的文本
                docIndex=getWordIndex(DocText).split(' ')###预处理后的文本单词索引


                tempList = []
                for i in range(len(doc_id_list)):
                    if(doc_id_list[i]==doc_id):

                        # print(doc_id_list[i])
                        # print(query_name_list[i])
                        # print(query_id_list[i])
                        tempString = doc_id_list[i] + ' ' + query_id_list[i] + ' ' + query_name_list[i] + '\n'
                        docfile.write(tempString)

                        for j in range(len(answer_query_id_list)):
                            if(answer_query_id_list[j]==query_id_list[i]):
                                # print(answer_query_id_list[j])
                                # print(query_id_list[i])
                                # print('query name:'+query_name_list[i]+' find query:'+DocText[int(query_beg_list[i]):int(query_end_list[i])+1].replace('\n',' '))

                                currentText = docText.replace('\n',' ')
                                currentQuery = query_name_list[i]
                                entityIndex,contentIndex,index_beg,index_end=getContentIndex(currentText,currentQuery,docIndex,doc_id)
                                queryIndexFile.write(query_id_list[i]+' '+contentIndex.strip(' ')+'\n')
                                queryIndexFile.write(query_id_list[i] + ' ' + entityIndex.strip(' ') + '\n')
                                contentNounIndex, _, _, _ = getContentNounIndex(currentText, currentQuery, docIndex, doc_id)
                                print('contentNounIndex:'+contentNounIndex)
                                print('entityIndex:'+entityIndex)
                                queryNounIndexFile.write(query_id_list[i] + ' ' + contentNounIndex.strip(' ') + '\n')
                                queryNounIndexFile.write(query_id_list[i] + ' ' + entityIndex.strip(' ') + '\n')





                                tempString = doc_id_list[i] + ' ' + answer_query_id_list[j] + ' ' + answer_query_name_list[j] +' '+answer_db_id_list[j]+' '+answer_db_name_list[j]+' beg='
                                indexString = doc_id_list[i] + ' ' + answer_query_id_list[j] + ' ' + answer_query_name_list[j] + ' ' + answer_db_id_list[j] + ' ' + answer_db_name_list[j] + ' index_beg=' + \
                                             str(index_beg) + ' index_end=' + str(index_end)
                                tpString = doc_id_list[i] + ' ' + answer_query_name_list[j] +' '+answer_db_id_list[j]+' '+answer_db_name_list[j]



                                docindexfile.write(indexString+'\n')
                                docindexfile.write(entityIndex+'\n')
                                docindexfile.write(contentIndex+'\n')


                                docfile.write(tempString+'\n')
                                print("tempString tempString:"+tempString)
                                tempList.append(tpString)
                                # if(answer_db_id_list[j].find('NIL')==-1):
                                #     if(OOOMap[answer_db_id_list[j]].find("没问题")==-1):
                                #         print(OOOMap[answer_db_id_list[j]])
                                #         print(tempString)

                                with open(docP + "\\" + doc_id + '.xml', encoding='utf-8') as textF:
                                    docText = textF.read()
                                soup = BeautifulSoup(docText, 'html.parser')
                                words = nltk.word_tokenize(soup.get_text())
                                word_tag = nltk.pos_tag(words)
                                newText = NewText(word_tag)
                                queryTextIndexFile.write(
                                    query_id_list[i] + ' ' + getWordIndex(newText).strip(' ') + '\n')
                                queryTextIndexFile.write(query_id_list[i] + ' ' + entityIndex.strip(' ') + '\n')
                                print("textIdex:" + getWordIndex(newText))

                tpList=set(tempList)
                for tp in tpList:
                    unidocfile.write(tp+'\n')

                docfile.close()



                with open(docP + "\\" + doc_id +'.xml', encoding='utf-8') as textF:
                    docText = textF.read()
                soup = BeautifulSoup(docText, 'html.parser')
                words = nltk.word_tokenize(soup.get_text())
                word_tag = nltk.pos_tag(words)
                newText = NewText(word_tag)
                textfile.write(newText+'\n')
                fre=DocWordfrequency(newText)
                for w in fre:
                    # wStr=
                    textfile.write(w + '\n')
                # print(newText)
                # print(fre)


            doc_line = docF.readline()

    # queryIndexFile.close()


    pass



if __name__=='__main__':

    year='2010'  #2009 2010 2011  trian2010
    testFlag=True
    readWordVecIndex()
    if(testFlag):
        docPath = u'H:\yaojuan\QUERY\\'+year+'\\eval\\test\DocFileName.txt'
        queryPath = u'H:\yaojuan\QUERY\\'+year+'\\eval\\tac_kbp_'+year+'_english_entity_linking_evaluation_queries.xml'
        answerPath = u'H:\yaojuan\QUERY\\'+year+'\\eval\\test\\answer.txt'
        dbIdNamePath = u'DBIdName.txt'
    else:
        #####train train train 2010 2010 2010
        docPath = u'H:\yaojuan\QUERY\\' + year + '\\training\\train\DocFileName.txt'
        queryPath = u'H:\yaojuan\QUERY\\' + year + '\\training\\tac_kbp_' + year + '_english_entity_linking_training_queries.xml'
        answerPath = u'H:\yaojuan\QUERY\\' + year + '\\training\\train\\answer.txt'
        dbIdNamePath = u'DBIdName.txt'


    readIdNameFile(dbIdNamePath)
    readQueryFile(queryPath)
    readAnswerFile(answerPath)
    findDocQueryAndDbAnswer(docPath, year,testFlag)

    pass














