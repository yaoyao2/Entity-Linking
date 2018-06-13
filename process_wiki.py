# coding=utf-8
import os
import logging
import sys
import re
import multiprocessing
import gensim

from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

def process_wiki(inp, outp):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)

    i = 0

    #output = open(outp, 'w', encoding='utf-8')
    output = open(outp, 'wt', encoding='utf-8')#使用 “t�?类型打开文件，字符串的形�?
    wiki = WikiCorpus(inp, lemmatize=False, dictionary={})
    for text in wiki.get_texts():
        #output.write(b' '.join(text).decode('utf-8') + '\n')
        output.write( " ".join('%s' %id for id in text) + '\n')#遍历list的元素，把他转化成字符串�?
        #output.write('\n')
        i = i + 1
        if i % 10000 == 0:
            logger.info('Saved ' + str(i) + ' articles')

    output.close()
    logger.info('Finished ' + str(i) + ' articles')

def remove_words(inp, outp):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)

    output = open(outp, 'w', encoding='utf-8')
    inp = open(inp, 'r', encoding='utf-8')

    for line in inp.readlines():
        ss = re.findall('[\n\s*\r\u4e00-\u9fa5]', line)
        output.write("".join(ss))
    logger.info("Finished removed words!")

def separate_words(inp, outp):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)


    output = open(outp, 'w', encoding='utf-8')
    inp = open(inp, 'r', encoding='utf-8')

    for line in inp.readlines():
        seg_list = jieba.cut(line.strip())
        output.write(' '.join(seg_list) + '\n')
    logger.info("finished separate words!")

# inp为输入语�?
def train_w2v_model(inp, outp1, outp2):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # LineSentence(inp)：应该是把word2vec训练模型的磁盘存储文件（model在内存中总是不踏实）转换成所需要的格式；对应的格式是参考上面的�?�?
    # size：是每个词的向量维度�?
    # window：是词向量训练时的上下文扫描窗口大小，窗口为5就是考虑�?个词和后5个词�?
    # min - count：设置最低频率，默认�?，如果一个词语在文档中出现的次数小于5，那么就会丢弃；
    # workers：是训练的进程数（需要更精准的解释，请指正），默认是当前运行机器的处理器核数。这些参数先记住就可以了�?

    model = Word2Vec(LineSentence(inp), size=100, window=5, min_count=2,
                     workers=multiprocessing.cpu_count())

    # outp1 为输出模�?
    model.save(outp1)

    # outp2为原始c版本word2vec的vector格式的模�?
    model.wv.save_word2vec_format(outp2, binary=False)

def main():
    #process_wiki('enwiki-latest-pages-articles.xml.bz2', 'wiki.en.text')
    #process_wiki('enwiki-20180320-pages-articles14.xml-p7697599p7744799.bz2', 'wiki.en.text')
    # remove_words('./data/wiki_cn_jian.txt', './data/wiki_cn_jian_removed.txt')
    # separate_words('./data/wiki_cn_jian_removed.txt', './data/wiki_cn_jian_sep_removed.txt')
    # train_w2v_model('./data/wiki_cn_jian_sep_removed.txt', './bin/300/w2v_model.bin', './bin/300/w2v_vector.bin')
    train_w2v_model('wiki.en.text', 'w2v_model_100.bin', 'w2v_vector_100.bin')


if __name__=='__main__':
    main()
    # model = gensim.models.Word2Vec.load('./bin/300/w2v_model.bin')
    # print(model.most_similar([u'李连�?, u'基金'], [u'成龙']))