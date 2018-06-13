#!/usr/bin/python
# -*- coding:utf8 -*-

def check(docPath,dbPath):
    db_id_list=[]
    db_name_list=[]
    count = 0
    with open(dbPath,encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:

            if (count % 2 == 0):
                db_id_list.append(line)
                # print(line)
            if (count % 2 == 1):
                db_name_list.append(line)

            count = count + 1
            line = f.readline().strip('\n')

        pass


    with open(docPath,encoding='utf-8') as docF:
        doc_line=docF.readline().strip('\n')
        while doc_line:
            pos=doc_line.find('E0')
            answerId=doc_line[pos:pos+8]

            findFlag=True
            if(len(answerId)==8):

                for i in range(len(db_id_list)):
                    db_id=db_id_list[i]
                    if(db_id==answerId):
                        # print("find!!! "+answerId)
                        # print(doc_line)
                        # print(answerId)
                        findFlag=False
                        break
                if(findFlag):
                    print(doc_line)
                    print(answerId)
                    print("not find!!! "+answerId)



            doc_line = docF.readline().strip('\n')



    pass




if __name__=='__main__':

    docPath=u'E:\mypython_Linking\data_handle\docQuery\doc_'
    dbPath=u'E:\mypython_Linking\data_handle\dbEntity\db_'
    check(docPath+'1.txt',dbPath+'1.txt')
    pass
