#coding=utf-8
import numpy
import tensorflow as tf
from keras.datasets import mnist
from keras.models import Sequential
import keras.backend as K
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
import matplotlib.pyplot as plt
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers import *
from keras.models import *
import data_load
import sys
# from CNN import data_load
from keras.utils.vis_utils import plot_model

# import os
# os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'
year=sys.argv[1]
test_query_path=sys.argv[2]
test_db_path=sys.argv[3]

#求余弦函数
def cosVector(x,y):
    if(len(x)!=len(y)):
        print('error input,x and y is not in the same space')
        return;
    result1=0.0;
    result2=0.0;
    result3=0.0;
    for i in range(len(x)):
        result1+=x[i]*y[i]   #sum(X*Y)
        result2+=x[i]**2     #sum(X*X)
        result3+=y[i]**2     #sum(Y*Y)
    #print("result is "+str(result1/((result2*result3)**0.5))) #结果显示
    return result1/((result2*result3)**0.5)



# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# load data
(query_train,query_name_train,db_train,db_name_train,lab_train) = data_load.readTrainAllData(local=False)
(query_test,query_name_test,db_test,db_name_test,lab_test) = data_load.readAllData(local=False,year=year,queryPath=test_query_path,dbPath=test_db_path)

# query_train = query_train.reshape(query_train.shape[0],query_train.shape[1],query_train.shape[2]).astype('float32')
# #query_name_train = query_name_train.reshape(query_name_train.shape[0],query_name_train.shape[1],query_name_train.shape[2]).astype('float32')
# query_test = query_test.reshape(query_test.shape[0],query_test.shape[1],query_test.shape[2]).astype('float32')
# db_train = db_train.reshape(db_train.shape[0],db_train.shape[1],db_train.shape[2]).astype('float32')
# db_test = db_test.reshape(db_test.shape[0],db_test.shape[1],db_test.shape[2]).astype('float32')
num_classes = 2


# #定义记录位置信息的共现变量
# pos=np.random.uniform(-0.01,0.01,size=(query_train.shape[1],query_train.shape[2]))
# POS=[]
# for i in range(query_train.shape[0]):
#     POS.append(pos)
# Pos=np.asarray(POS)
# print(Pos.shape)
# query_pos_train=np.concatenate((query_train,Pos),axis=2)
#
# POS=[]
# for i in range(query_test.shape[0]):
#     POS.append(pos)
# Pos=np.asarray(POS)
# print(Pos.shape)
# query_pos_test=np.concatenate((query_test,Pos),axis=2)

# 自定义query模型
query_input=Input(shape=(query_train.shape[1], query_train.shape[2]))
query_conv1=Conv1D(30, 5, padding='valid', activation='relu')(query_input)
query_maxp1=MaxPooling1D(pool_size=2)(query_conv1)
query_drop1=Dropout(0.4)(query_maxp1)
query_conv2=Conv1D(15, 3, activation='relu')(query_drop1)
query_maxp2=MaxPooling1D(pool_size=2)(query_conv2)
query_drop2=Dropout(0.4)(query_maxp2)
query_flat1=Flatten()(query_drop2)

query_name_input=Input(shape=(query_name_train.shape[1],query_name_train.shape[2]))
query_name_flat1=Flatten()(query_name_input)
query_union=Concatenate()([query_flat1,query_name_flat1])

query_dens1=Dense(128, activation='relu')(query_union)
query_drop3=Dropout(0.4)(query_dens1)
query_dens2=Dense(50, activation='relu')(query_drop3)
query_drop4=Dropout(0.4)(query_dens2)
query_model=Dense(20, activation='softmax',name='query_model')(query_drop4)

# 自定义db模型
db_input=Input(shape=(db_train.shape[1], db_train.shape[2]))
db_conv1=Conv1D(30, 5, padding='valid', activation='relu')(db_input)
db_maxp1=MaxPooling1D(pool_size=2)(db_conv1)
db_drop1=Dropout(0.4)(db_maxp1)
db_conv2=Conv1D(15, 3, activation='relu')(db_drop1)
db_maxp2=MaxPooling1D(pool_size=2)(db_conv2)
db_drop2=Dropout(0.4)(db_maxp2)
db_flat1=Flatten()(db_drop2)

db_name_input=Input(shape=(db_name_train.shape[1],db_name_train.shape[2]))
db_name_flat1=Flatten()(db_name_input)
db_union=Concatenate()([db_flat1,db_name_flat1])

db_dens1=Dense(128, activation='relu')(db_union)
db_drop3=Dropout(0.4)(db_dens1)
db_dens2=Dense(50, activation='relu')(db_drop3)
db_drop4=Dropout(0.4)(db_dens2)
db_model=Dense(20, activation='softmax',name='db_model')(db_drop4)

print(query_model.shape)
print(db_model.shape)

# x=Concatenate()([query_model,db_model])
# We stack a deep densely-connected network on top
x = Multiply(name='Multiply')([query_model,db_model])
x = Dense(10, activation='relu')(x)
# x = Dense(64, activation='relu')(x)
# x = Dense(64, activation='relu')(x)

# And finally we add the main logistic regression layer
main_output = Dense(1, activation='sigmoid', name='main_output')(x)


model = Model(inputs=[query_input,query_name_input,db_input,db_name_input],outputs=main_output)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# new_model = Dot([query_model,db_model])

#
# plot_model(model,to_file='myCNN_model_1.png', show_shapes=True)

# Fit the model
model.fit([query_train,query_name_train,db_train,db_name_train],lab_train,  epochs=100, batch_size=200, verbose=2)
# Final evaluation of the model
scores = model.evaluate([query_test,query_name_test,db_test,db_name_test], lab_test, verbose=0)
print("Large CNN Error: %.2f%%" % (100 - scores[1] * 100))

#save model
model.save('myCNN_model_1.h5')

# 已有的model在load权重过后
# 取某一层的输出为输出新建为model，采用函数模型
query_layer_model = Model(inputs=model.input,
                           outputs=model.get_layer('query_model').output)
db_layer_model = Model(inputs=model.input,
                        outputs=model.get_layer('db_model').output)

# 以这个model的预测值作为输出
query_output = query_layer_model.predict([query_test,query_name_test,db_test,db_name_test])
db_output = db_layer_model.predict([query_test,query_name_test,db_test,db_name_test])


model_output = model.predict([query_test,query_name_test,db_test,db_name_test])
print(model_output.shape)

predictFile=open(year+'predict.txt','w',encoding='utf-8')
for i in range(model_output.shape[0]):
    x=model_output[i]
    pre=1 / float(1 + np.exp(- x))
    predictFile.write(str(pre)+'\n')
predictFile.close()


#计算query_output和db_output的余弦值，用60*1的向量存储
rows=query_output.shape[0] #行数
cols=query_output.shape[1] #列数
cosResult= [[0]*1 for i in range(rows)]


for i in range(rows):
    cosResult[i][0]=cosVector(query_output[i], db_output[i])

#print(cosResult)

file=open(year+'_cos.txt','w')
for i in cosResult:
  file.write(str(i).replace('[','').replace(']','')+'\n')  #\r\n为换行符

file.close()
