#coding=utf-8
#加载Google训练的词向量
import numpy as np
import tensorflow as tf

queryIndexMap=dict()
queryNameIndexMap=dict()
dbIndexMap=dict()
dbNameIndexMap=dict()
dbTrainIndexMap=dict()
dbNameTrainIndexMap=dict()
queryTrainIndexMap=dict()
queryNameTrainIndexMap=dict()


# 加载所有的词向量
def load_word_vectors(file_path):

    print ('loading word vectors...')
    f = open(file_path, 'r', encoding='utf-8')
    m =f.readlines()
    i = 0
    for li in m:
        m[i] = m[i].strip().split(' ')
        i = i + 1

    num_words=int(len(m))#词向量表的大小
    vec_len=int(len(m[0][1:]))#词向量的大小
    print (num_words,vec_len)
    words = []
    word_vecs = np.zeros((num_words + 1, vec_len))#词向量表初始化为全0，在0位置处，表示找到的词的向量为0

    for i in range(num_words):
        if i == 0:
            words.append(m[i][0])
        words.append(m[i][0])
        word_vecs[i + 1] = np.array(m[i][1:],dtype=np.float32)

    f.close()
    print ('done.')

    return words, word_vecs

def readQueryIndex(local,year,queryPath):
    global queryIndexMap
    global queryNameIndexMap
    if(local):
        path='H:\yaojuan\QUERY\\'+year+'\eval\\test\\test_queryIndex.txt'
    else:
        path = queryPath
    with open(path,encoding='utf-8') as f:
        line=f.readline().strip(' ').strip('\n')
        lineCount=0
        while line:
            if(lineCount%2==0):
                ##第一行，上下文
                queryId=line.split(' ')[0]
                queryIndex=line[len(line.split(' ')[0])+1:].strip(' ')
                queryIndexMap[queryId]=queryIndex
            if(lineCount%2==1):
                ##第二行，name
                queryId=line.split(' ')[0]
                queryIndex=line[len(line.split(' ')[0])+1:].strip(' ')
                queryNameIndexMap[queryId]=queryIndex
            lineCount=lineCount+1
            line=f.readline().strip(' ').strip('\n')
    pass

def readMinDBIndex(local,year,dbPath):
    global dbIndexMap
    global dbNameIndexMap
    if(local):
        path='H:\yaojuan\QUERY\\'+year+'\eval\\test_mindbIndex.txt'
    else:
        path = dbPath

    with open(path,encoding='utf-8') as f:
        line = f.readline().strip('\n').strip(' ')
        lineCount=0
        while line:
            if(lineCount%2==0):
                dbId = line.split(' ')[0]
                dbIndex = line[len(line.split(' ')[0]) + 1:]
                dbIndexMap[dbId] = dbIndex
            if(lineCount%2==1):
                dbId = line.split(' ')[0]
                dbIndex = line[len(line.split(' ')[0]) + 1:]
                dbNameIndexMap[dbId] = dbIndex

            lineCount=lineCount+1
            line = f.readline().strip('\n').strip(' ')

    pass

def readTrainMinDBIndex(local):
    global dbTrainIndexMap
    global dbNameTrainIndexMap
    if(local):
        ####将2014的训练数据当做模型的训练集
        path='H:\yaojuan\QUERY\\2014\\training\\train_mindbIndex.txt'
    else:
        path = 'train_mindbIndex.txt'

    with open(path,encoding='utf-8') as f:
        line = f.readline().strip(' ').strip('\n')
        lineCount=0
        while line:
            if(lineCount%2==0):
                dbId = line.split(' ')[0]
                dbIndex = line[len(line.split(' ')[0]) + 1:]
                dbTrainIndexMap[dbId] = dbIndex
            if (lineCount%2==1):
                dbId = line.split(' ')[0]
                dbIndex = line[len(line.split(' ')[0]) + 1:]
                dbNameTrainIndexMap[dbId] = dbIndex

            lineCount=lineCount+1
            line = f.readline().strip(' ').strip('\n')

    pass

def readTrainQueryIndex(local):
    global queryTrainIndexMap
    global queryNameTrainIndexMap
    if(local):
        ####将2014的训练数据当做模型的训练集
        path='H:\yaojuan\QUERY\\2014\\training\\train\\train_queryIndex.txt'
    else:
        path = 'train_queryNounIndex.txt'
    with open(path,encoding='utf-8') as f:
        line=f.readline().strip(' ').strip('\n')
        lineCount=0
        while line:
            if(lineCount%2==0):
                queryId=line.split(' ')[0]
                queryIndex=line[len(line.split(' ')[0])+1:].strip(' ')
                queryTrainIndexMap[queryId]=queryIndex
            if(lineCount%2==1):
                queryId = line.split(' ')[0]
                queryIndex = line[len(line.split(' ')[0]) + 1:].strip(' ')
                queryNameTrainIndexMap[queryId] = queryIndex


            lineCount=lineCount+1
            line=f.readline().strip(' ').strip('\n')
    pass

def readTrainAllData(local):
    words, word_vecs = load_word_vectors(u'glove.6B.100d.txt')
    if(local):
        #######这个query——entity对
        alldataPath = 'E:\mypython_Linking\\data_handle\\train_all_data.txt'
    else:
        alldataPath = 'train_all_data.txt'
    ####训练集不需要传year年份
    readTrainQueryIndex(local)
    readTrainMinDBIndex(local)
    queryIdList=[]
    queryIndexList=[]
    queryNameIndexList=[]
    dbIdList=[]
    dbIndexList=[]
    dbNameIndexList=[]
    lableList=[]
    maxLength=0
    minLength=1000
    lineCount=0
    with open(alldataPath, encoding='utf-8') as f:
        line = f.readline().strip('\n')

        while line:
            lineCount=lineCount+1
            dbId = line.split(' ')[1]
            if (len(dbTrainIndexMap[dbId].strip(' ').split(' ')) > maxLength):
                maxLength = len(dbTrainIndexMap[dbId].strip(' ').split(' '))
            if (len(dbTrainIndexMap[dbId].strip(' ').split(' ')) < minLength):
                minLength = len(dbTrainIndexMap[dbId].strip(' ').split(' '))
            line = f.readline().strip('\n')
    print('train_maxLength=' + str(maxLength))
    print('train_minLength=' + str(minLength))
    print('train_lineCount=' + str(lineCount))
    # trainLen = lineCount // 3


    with open(alldataPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        lineCount=0
        while line:
            lineCount=lineCount+1
            line=line.split(' ')
            queryId=line[0]
            dbId=line[1]
            lable=line[2]
            # print('queryId='+queryId)
            # print('queryIndex='+queryIndexMap[queryId])
            # print('dbId='+dbId)
            # print('dbIndex='+dbIndexMap[dbId])
            # print('lable='+lable)
            queryIdList.append(queryId)
            queryIndex=queryTrainIndexMap[queryId].strip(' ').split(' ')
            queryNameIndex=queryNameTrainIndexMap[queryId].strip(' ').split(' ')
            textVec=[]
            for i in queryIndex:
                textVec.append(word_vecs[int(i)])
            queryIndexList.append(np.asarray(textVec,dtype=np.float32))

            nameVec=[]
            for i in queryNameIndex:
                nameVec.append(word_vecs[int(i)])
            queryNameIndexList.append(np.asarray(nameVec,dtype=np.float32).mean(axis=0))


            dbIdList.append(dbId)
            dbIndex=dbTrainIndexMap[dbId]
            dbNameIndex = dbTrainIndexMap[dbId].strip(' ').split(' ')
            for i in range(len(dbTrainIndexMap[dbId].strip(' ').split(' ')),160):
                dbIndex=dbIndex.strip(' ')+' 0'
            dbIndex=dbIndex.strip(' ').split(' ')

            dbVec=[]
            for i in dbIndex:
                dbVec.append(word_vecs[int(i)])
            dbIndexList.append(np.asarray(dbVec,dtype=np.float32))

            nameVec = []
            for i in dbNameIndex:
                nameVec.append(word_vecs[int(i)])
            dbNameIndexList.append(np.asarray(nameVec, dtype=np.float32).mean(axis=0))

            lableList.append(lable)

            # if(lineCount>=90):
            #
            #     break

            line=f.readline().strip('\n')

    query=np.asarray(queryIndexList,dtype=np.float32)
    queryName=np.asarray(queryNameIndexList,dtype=np.float32)[:,np.newaxis,:]
    db=np.asarray(dbIndexList,dtype=np.float32)
    dbName=np.asarray(dbNameIndexList,dtype=np.float32)[:,np.newaxis,:]
    lab=np.asarray(lableList,dtype=np.float32)

    print(query.shape)
    print(queryName.shape)
    print(db.shape)
    print(dbName.shape)
    print(lab.shape)


    return (query,queryName,db,dbName,lab)







def readAllData(local,year,queryPath,dbPath):
    words, word_vecs = load_word_vectors(u'glove.6B.100d.txt')
    if(local):
        alldataPath = 'H:\yaojuan\QUERY\\'+year+'\eval\\test_all_data.txt'
    else:
        alldataPath = year+'_test_all_data.txt'
    readQueryIndex(local,year,queryPath)
    readMinDBIndex(local,year,dbPath)
    queryIdList=[]
    queryIndexList=[]
    queryNameIndexList=[]
    dbIdList=[]
    dbIndexList=[]
    dbNameIndexList=[]
    lableList=[]
    maxLength=0
    minLength=1000
    lineCount=0
    with open(alldataPath, encoding='utf-8') as f:
        line = f.readline().strip('\n')

        while line:
            lineCount=lineCount+1
            dbId = line.split(' ')[1]
            if (len(dbIndexMap[dbId].strip(' ').split(' ')) > maxLength):
                maxLength = len(dbIndexMap[dbId].strip(' ').split(' '))
            if (len(dbIndexMap[dbId].strip(' ').split(' ')) < minLength):
                minLength = len(dbIndexMap[dbId].strip(' ').split(' '))
            # if(lineCount>=90):
            #     break
            line = f.readline().strip('\n')
    print('test_maxLength=' + str(maxLength))
    print('test_minLength=' + str(minLength))
    print('test_lineCount=' + str(lineCount))


    with open(alldataPath,encoding='utf-8') as f:
        line=f.readline().strip('\n')
        lineCount=0
        while line:
            lineCount=lineCount+1
            if(lineCount>0):
                line=line.split(' ')
                queryId=line[0]
                dbId=line[1]
                lable=line[2]
                # print('queryId='+queryId)
                # print('queryIndex='+queryIndexMap[queryId])
                # print('dbId='+dbId)
                # print('dbIndex='+dbIndexMap[dbId])
                # print('lable='+lable)
                queryIdList.append(queryId)
                queryIndex=queryIndexMap[queryId].strip(' ').split(' ')
                queryNameIndex=queryNameIndexMap[queryId].strip(' ').split(' ')
                textVec=[]
                for i in queryIndex:
                    textVec.append(word_vecs[int(i)])
                queryIndexList.append(np.asarray(textVec,dtype=np.float32))

                nameVec = []
                for i in queryNameIndex:
                    nameVec.append(word_vecs[int(i)])
                queryNameIndexList.append(np.asarray(nameVec, dtype=np.float32).mean(axis=0))

                dbIdList.append(dbId)
                dbIndex=dbIndexMap[dbId]
                dbNameIndex=dbNameIndexMap[dbId].strip(' ').split(' ')
                for i in range(len(dbIndexMap[dbId].strip(' ').split(' ')),160):
                    dbIndex=dbIndex.strip(' ')+' 0'
                dbIndex=dbIndex.strip(' ').split(' ')
                dbVec=[]
                for i in dbIndex:
                    dbVec.append(word_vecs[int(i)])
                dbIndexList.append(np.asarray(dbVec,dtype=np.float32))

                nameVec = []
                for i in dbNameIndex:
                    nameVec.append(word_vecs[int(i)])
                dbNameIndexList.append(np.asarray(nameVec, dtype=np.float32).mean(axis=0))

                lableList.append(lable)
                # if(lineCount>=200000):
                #
                #     break

            line=f.readline().strip('\n')

    query=np.asarray(queryIndexList,dtype=np.float32)
    queryName=np.asarray(queryNameIndexList,dtype=np.float32)[:,np.newaxis,:]
    db=np.asarray(dbIndexList,dtype=np.float32)
    dbName=np.asarray(dbNameIndexList,dtype=np.float32)[:,np.newaxis,:]
    lab=np.asarray(lableList,dtype=np.float32)
    print(query.shape)
    print(queryName.shape)
    print(db.shape)
    print(dbName.shape)
    print(lab.shape)


    return (query,queryName,db,dbName,lab)





if __name__=='__main__':
    # readQueryIndex(True) #输出显示test_query的上下文长度是20
    # readMinDBIndex(True) #输出显示test_db的上下文长度是768
    # readTrainQueryIndex(True) #输出显示train_query的上下文长度是20
    # readTrainMinDBIndex(True) #输出显示train_db的上下文长度是1478


    # readAllData(local=True,year='2014')
    readTrainAllData(local=True)
    # readTrainAllData(local=True)
    pass












####################################################################################################

    # SentLength=10
    #
    # sentence1='I love you very much x_x'
    # sentence2='I like you'
    #
    # s_vec1 = sentence2vec(sentence1,SentLength)
    # s_vec2 = sentence2vec(sentence2,SentLength)
    #
    # # print(s_vec1)
    # print(s_vec1.shape)
    #
    # # 准备已有数据
    # x_data1 = tf.constant(s_vec1[np.newaxis,:,:,np.newaxis],dtype=tf.float32)
    # x_data2 = tf.constant(s_vec2[np.newaxis,:,:,np.newaxis],dtype=tf.float32)
    # y_data = [1]
    # print(x_data1.shape)
    #
    # # 定义placeholder
    # x1 = tf.placeholder(tf.float32, [None, 1])
    # x2 = tf.placeholder(tf.float32, [None, 1])
    # y = tf.placeholder(tf.float32, [None, 1])
    #
    #
    # # [batch, in_height, in_width, in_channels] 1,20,50,1
    # input_arg1 = tf.Variable(s_vec1)
    # input_arg2 = tf.Variable(s_vec2)
    # # [filter_height, filter_width, in_channels, out_channels]
    # filter_arg1 = tf.Variable(tf.ones([3, 3, 1, 1]))
    # filter_arg2 = tf.Variable(tf.ones([3, 3, 1, 1]))
    # op1 = tf.nn.relu(tf.nn.conv2d(x_data1, filter_arg1, strides=[1, 1, 4, 1], use_cudnn_on_gpu=False, padding='SAME'))
    # pool1=tf.nn.max_pool(op1, ksize=[1, 2, 4, 1],strides=[1, 2, 4, 1], padding='SAME')
    # # softmax1=tf.nn.softmax(pool1)
    #
    # # connected=tf.nn.con
    # # op2 = tf.nn.conv2d(input_arg2, filter_arg2, strides=[1, 2, 2, 1], use_cudnn_on_gpu=False, padding='SAME')
    # # # 求模`
    # # x1_norm = tf.sqrt(tf.reduce_sum(tf.square(op1), axis=2))
    # #
    # # x2_norm = tf.sqrt(tf.reduce_sum(tf.square(op2), axis=2))
    # # x1_x2=tf.reduce_sum(tf.multiply(x1, x2), axis=2)
    # #
    # # cosin = x1_x2 / (x1_norm * x2_norm)
    # #
    # # cosin1 = tf.pide(x1_x2, tf.multiply(x1_norm, x2_norm))
    # #
    # #
    #
    #
    #

    # with tf.Session() as a_sess:
    #     a_sess.run(tf.global_variables_initializer())
    #     # op1,op2,a, b, c, d, e = a_sess.run([op1,op2,x1_norm, x2_norm, x1_x2, cosin, cosin1])
    #
    #
    #     print("----------{}---------".format("case1"))
    #     a_op1=a_sess.run(pool1)
    #     writer = tf.summary.FileWriter('tensorflow/', a_sess.graph)
    #     print(a_op1)
    #     print(a_op1.shape)
    #     KKK=tf.reshape(a_op1,(1,20))
    #     print(KKK)
    #
    #     print('---------------------\n\n')
    #
    # pass