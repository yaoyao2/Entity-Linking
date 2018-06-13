#coding=utf-8



def produce_entity_index(entity2idPath,DB_id_index_Path,allDBIdexPath):

    idMap=dict()
    with open(entity2idPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            id=line.split(' ')[0][3:]
            index=int(line.split(' ')[1])
            # print(id)
            # print(index+1)
            idMap[id]=index+1
            line=f.readline().strip('\n')

    dbf=open(allDBIdexPath,'w',encoding='utf-8')
    with open(DB_id_index_Path,encoding='utf-8') as f:
        line=f.readline().strip('\n').strip(' ')
        lineCount=0
        totalCount=0
        nolinkCount=0
        while line:
            lineCount=lineCount+1
            Ids=line.split(' ')
            tempStr=Ids[0]
            if(len(Ids)==1):
                tempStr=tempStr+' '+str(idMap[Ids[0]])
                dbf.write(tempStr+'\n')
                dbf.write(tempStr+'\n')
                nolinkCount=nolinkCount+1
            else:
                for i in range(len(Ids)):
                    if(Ids[i]!='E0006472' and Ids[i]!='E0186505' and Ids[i]!='E0532473'):
                        totalCount = totalCount + 1
                        tempStr=tempStr+' '+str(idMap[Ids[i]])
                dbf.write(tempStr.strip(' ') + '\n')
                dbf.write(Ids[0]+' '+str(idMap[Ids[0]])+'\n')
            print(tempStr)


            line=f.readline().strip('\n').strip(' ')
    print('average link='+str(int(totalCount/lineCount)))
    print(nolinkCount)


    pass









if __name__=='__main__':


    # entity2idPath='E:\mypython_Linking\CNN\entityId.txt'
    # DB_id_index_Path='E:\mypython_Linking\CNN\min_DB_id_index.txt'
    # allDBIdexPath = 'E:\mypython_Linking\CNN\min_DBIndex.txt'
    # produce_entity_index(entity2idPath,DB_id_index_Path,allDBIdexPath)


    ###############bu no link entity##############
    entity2idPath = 'E:\mypython_Linking\CNN\entityId_bu.txt'
    DB_id_index_Path = 'E:\mypython_Linking\CNN\min_DB_id_index_bu.txt'
    allDBIdexPath = 'E:\mypython_Linking\CNN\min_DBIndex_bu.txt'####生成新文件
    produce_entity_index(entity2idPath, DB_id_index_Path, allDBIdexPath)

    pass