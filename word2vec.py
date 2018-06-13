#! -*- coding=utf-8 -*-
from gensim.models import word2vec
import logging
# 主程序
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus(u"Text8.txt") #加载语料
#模型初始化S
model = word2vec.Word2Vec(sentences, size=50) #训练skip-gram模型; 默认window=5
model2 = word2vec.Word2Vec("hello wrold! hello The training algorithms were originally ported from the C package", size=50, window=5, min_count=5, workers=4)
print "--------/n"
print "--------/n"
y1 = model.similarity("woman", "man")
print u"woman和man的相似度为：", y1
print "--------/n"
print "--------/n"
y2 = model.most_similar("good", topn=20)  # 20个最相关的
print u"和good最相关的词有：/n"
for item in y2:
    print item[0], item[1]
print "--------/n"
print "--------/n"

# print ' "boy" is to "father" as "girl" is to ...? /n'
# y3 = model.most_similar(['girl', 'father'], ['boy'], topn=3)
# for item in y3:
#     print item[0], item[1]
# print "--------/n"
# print "--------/n"
#
# y4 = model.doesnt_match("breakfast cereal dinner lunch".split())
# print u"不合群的词：", y4
# print "--------/n"
# print "--------/n"
#
# y5 = model.init_sims()
#
model.wv.save_word2vec_format('vector_50.txt')
# #model = word2vec.Word2Vec.load_word2vec_format('/tmp/vectors.bin', binary=True)
# print "--------/n"
# print "--------/n"
#
# model.most_similar(['girl', 'father'], ['boy'], topn=3)
# print "--------/n"
# print "--------/n"
#
# more_examples = ["he his she", "big bigger bad", "going went being"]
# for example in more_examples:
#     a, b, x = example.split()
#     predicted = model.most_similar([x, b], [a])[0][0]
#     print "'%s' is to '%s' as '%s' is to '%s'" % (a, b, x, predicted)
# print "--------/n"
# print "--------/n"
#
# y6=model.wv['red']  # numpy vector of a word
# print y6
#
# y7=model.wv['white']  # numpy vector of a word
# print y7
#
# y8 = model.similarity("yes", "no")
# print y8
#
# y9 = model.similarity("color", "white")
# print y9
#
# y10 = model.similarity("red", "color")
# print y10