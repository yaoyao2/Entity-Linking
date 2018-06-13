#!/usr/bin/python
# -*- coding:utf8 -*-


T=0  #待链接实体总数（答案）
T1=0  #待链接实体NIL总数（答案）
T2=0  #待链接实体NOT_NIL总数（答案）
S=0  #待链接实体总数（自己）
S1=0  #待链接实体NIL总数（自己）
S2=0  #待链接实体NOT_NIL总数（自己）

NIL_Dui=0  #自己判空，且判对
NER_Dui=0  #自己判非空，且链接对


def get_T_S(answerPath):
    global T,T1,T2
    global S,S1,S2
    global NIL_Dui,NER_Dui
    with open(answerPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        lineCount=0
        while line:
            if(lineCount%2==0):
                TempLine=line
            if(lineCount%2==1):
                T=T+1
                S=S+1
                ans = line.split(' ')[0]
                if(line.find('NIL')==-1):
                    print(line)
                ansNum = int(line.split(' ')[1])
                if(ans.find('NIL')==-1):
                    ####NOT_NIL
                    T2=T2+1
                else:
                    ####NIL
                    T1=T1+1

                if(ansNum==0):
                    ####自己判空NIL
                    S1=S1+1
                    if(ans.find('NIL')!=-1):
                        # 自己判空，且判对
                        NIL_Dui=NIL_Dui+1
                else:
                    ####自己判非空NOT_NIL
                    S2=S2+1
                    #if(ans==line.split(' ')[2]):
                    if (int(line.split(' ')[1])<=5):
                        # 自己判非空，且链接对
                        NER_Dui=NER_Dui+1

            lineCount = lineCount + 1
            line=f.readline().strip('\n')



if __name__=='__main__':

    year='2009'; fileNum=3695
    # year='2010'; fileNum=2231
    # year='2011'; fileNum=2231
    # year='2012'; fileNum=2016
    # year='2013'; fileNum=1820
    # year='2014'; fileNum=138
    for i in range(fileNum):
        answerPath='H:\yaojuan\QUERY\\'+year+'\\eval\\test_dbEntity\db_new_'+str(i+1)+'.txt'
        # answerPath = 'H:\yaojuan\QUERY\\' + year + '\\eval\\test_dbEntity\db_' + str(i + 1) + '.txt'
        # answerPath = 'H:\yaojuan\QUERY\\2014\eval\\test_dbEntity\db_' + str(i + 1) + '.txt'
        get_T_S(answerPath)
    print(' 总   空   非空')
    print(T,T1,T2)
    print(S,S1,S2)
    print(NIL_Dui+NER_Dui,NIL_Dui,NER_Dui)
    print(NER_Dui/T2)
    # print(NIL_Dui/T1)
    Micro_accuracy_avrage=(NIL_Dui+NER_Dui)/T*100
    Precision=NER_Dui/S2*100
    Recall=NER_Dui/T2*100
    F1=2*Precision*Recall/(Precision+Recall)
    print('Micro_accuracy_avrage:'+str(Micro_accuracy_avrage)+'%')
    print('Precision:'+str(Precision)+'%')
    print('Recall:'+str(Recall)+'%')
    print('F1:'+str(F1)+'%')



    pass