#coding=utf-8
#加载Google训练的词向量
IdSet=set()

def readFile():
    global IdSet
    with open(u'H:\yaojuan\QUERY\\2014\\training\\train_mindbIndex.txt',encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            dbId=line.split(' ')[0]
            print(dbId)
            IdSet.add(dbId)
            line=f.readline().strip('\n')
    with open(u'H:\yaojuan\QUERY\\2014\\eval\\test_mindbIndex.txt',encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            dbId=line.split(' ')[0]
            print(dbId)
            IdSet.add(dbId)
            line=f.readline().strip('\n')
    with open(u'H:\yaojuan\QUERY\\2013\\eval\\test_mindbIndex.txt', encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:
            dbId = line.split(' ')[0]
            print(dbId)
            IdSet.add(dbId)
            line = f.readline().strip('\n')
    with open(u'H:\yaojuan\QUERY\\2012\\eval\\test_mindbIndex.txt', encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:
            dbId = line.split(' ')[0]
            print(dbId)
            IdSet.add(dbId)
            line = f.readline().strip('\n')
    with open(u'H:\yaojuan\QUERY\\2011\\eval\\test_mindbIndex.txt', encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:
            dbId = line.split(' ')[0]
            print(dbId)
            IdSet.add(dbId)
            line = f.readline().strip('\n')
    with open(u'H:\yaojuan\QUERY\\2010\\eval\\test_mindbIndex.txt', encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:
            dbId = line.split(' ')[0]
            print(dbId)
            IdSet.add(dbId)
            line = f.readline().strip('\n')
    with open(u'H:\yaojuan\QUERY\\2009\\eval\\test_mindbIndex.txt', encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:
            dbId = line.split(' ')[0]
            print(dbId)
            IdSet.add(dbId)
            line = f.readline().strip('\n')
    with open(u'H:\yaojuan\QUERY\\2010\\training\\train_mindbIndex.txt', encoding='utf-8') as f:
        line = f.readline().strip('\n')
        while line:
            dbId = line.split(' ')[0]
            print(dbId)
            IdSet.add(dbId)
            line = f.readline().strip('\n')



    ########bu no link entity#########
    tempStoreIdSet=set()
    with open(u'E:\mypython_Linking\CNN\\bu_link0.8.txt',encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            dbIds = line.split(' ')
            for id in dbIds:
                if(id not in IdSet):
                    IdSet.add(id)
                    tempStoreIdSet.add(id)
            line=f.readline().strip('\n')

    ALLPath = 'H:\yaojuan\QUERY\juan\zuizhongkuochong\DB_id_index.txt'
    linkMap=dict()
    with open(ALLPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            id=line.split(' ')[0]
            linkMap[id]=line[len(id)+1:].strip(' ')
            # print("YYYYYYYYYYYYYYY")
            # print(line[len(id)+1:])
            line=f.readline().strip('\n')

    while len(tempStoreIdSet)!=1:
        ###E0006472没有
        print(len(tempStoreIdSet))
        print(tempStoreIdSet)
        # tempStoreIdSet.remove('')
        IdList=[]
        for key in tempStoreIdSet:
            IdList.append(key)

        for key in IdList:
            tempStoreIdSet.remove(key)
            if(key!='E0753362'):
                line=linkMap[key]
                if(len(line)>2):
                    line=linkMap[key].split(' ')
                    for i in line:
                        if(i not in IdSet):
                            IdSet.add(i)
                            tempStoreIdSet.add(i)





def produceMyEntityVec(path,newPath,idPath,DB_id_index_Path,min_DB_id_index_Path):
    IdMap=dict()
    with open(path,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        while line:
            id=line.split(' ')[0]
            IdMap[id]=line
            line=f.readline().strip('\n')

    linkMap=dict()
    with open(DB_id_index_Path,encoding='utf-8') as f:
        line=f.readline().strip('\n').strip(' ')
        while line:
            id = line.split(' ')[0]
            linkMap[id]=line
            line=f.readline().strip('\n').strip(' ')

    newf=open(newPath,'w',encoding='utf-8')
    idf = open(idPath,'w',encoding='utf-8')
    minf = open(min_DB_id_index_Path,'w',encoding='utf-8')
    IdCount=0
    for id in IdSet:
        newf.write(IdMap[id]+'\n')
        idf.write('/m/'+id+' '+str(IdCount)+'\n')
        IdCount=IdCount+1
        minf.write(linkMap[id]+'\n')


if __name__=='__main__':

    ######
    # readFile()
    # print(len(IdSet))
    # if 'E0487663' in IdSet:
    #     print("E0487663 E0487663 E0487663 E0487663")
    # else:
    #     print('WAN WAN WAN WAN WAN WAN')
    # path = 'E:\mypython_Linking\CNN\entityvec.txt'
    # newPath = 'E:\mypython_Linking\CNN\my_entity_vecs.txt'
    # idPath = 'E:\mypython_Linking\CNN\entityId.txt'
    # DB_id_index_Path = 'H:\yaojuan\QUERY\juan\zuizhongkuochong\DB_id_index.txt'
    # min_DB_id_index_Path = 'E:\mypython_Linking\CNN\min_DB_id_index.txt'
    # produceMyEntityVec(path,newPath,idPath,DB_id_index_Path,min_DB_id_index_Path)


    #####################bu no link entity ########################
    readFile()
    # IdSet.remove('E0753362')
    print(len(IdSet))

    if 'E0487663' in IdSet:
        print("E0487663 E0487663 E0487663 E0487663")
    else:
        print('WAN WAN WAN WAN WAN WAN')
    # path = 'E:\mypython_Linking\CNN\entityvec.txt'#总的实体向量，有八十多万 ###读
    path = 'H:\yaojuan\QUERY\juan\zuizhongkuochong\entityvec.txt'#总的实体向量，有八十多万 ###读
    newPath = 'E:\mypython_Linking\CNN\my_entity_vecs_bu.txt'###生成的新文件
    idPath = 'E:\mypython_Linking\CNN\entityId_bu.txt'###生成的新文件
    DB_id_index_Path = 'H:\yaojuan\QUERY\juan\zuizhongkuochong\DB_id_index_bu.txt'###读
    min_DB_id_index_Path = 'E:\mypython_Linking\CNN\min_DB_id_index_bu.txt'###生成的新文件
    produceMyEntityVec(path, newPath, idPath, DB_id_index_Path, min_DB_id_index_Path)




