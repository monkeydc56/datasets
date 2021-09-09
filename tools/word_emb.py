import numpy as np
# from keras.preprocessing.text import Tokenizer
import pandas as pd
import Tag
import re
from nltk.corpus import stopwords
# tokenizer = Tokenizer()
# doc = pd.read_table(r"C:\Users\哈哈\Desktop\t.txt",header=None)
doc = pd.read_table(r"C:\Users\哈哈\PycharmProjects\datasets\aapd\doc",header=None)#文本文件位置
doc = doc.values.tolist()
embeddings_dict = Tag.Glove('D:\glove\.vector_cache\glove.6B.300d.txt')

def split(doc):#去除文本中的符号数字停用词
    doc_new_mid = []
    for i in range(len(doc)):
        for l in doc[i]:#去除数字与符号
            s = re.sub("[\d]", '', str(l))
            string = re.sub(r"[\s+\.\!\/_,$%^*(+\'\\']+|[+——！，。？、~@#￥%……&*()（）\[\]]+", " ", s)
            list = string.split()
            fillist = [word for word in list if word not in stopwords.words('english')]#去除停用词
        doc_new_mid.append(fillist)

    return doc_new_mid


def word_emb(doc_new_mid):
    res = (max(doc_new_mid, key=len, default=''))
    res = len(res)  # 最长句子长度
    word_victor = []
    for i in range(len(doc_new_mid)):
        lenth = len(doc_new_mid[i])
        a = res - lenth
        pad = ['<unk>'] * a
        doc_new_mid[i].extend(pad)  # 为每句话填充0
        #for j in range(len(doc_new_mid[i])):
        word_victor_mid = []
        for word in doc_new_mid[i]:
            # print(word)
            if word not in embeddings_dict.keys():
                word_vec = embeddings_dict['<unk>']
            else:
                word_vec = embeddings_dict[word]
            word_victor_mid.append(word_vec.tolist())  # 由每个词向量组成的词向量矩阵，可以直接输入bilstm
        word_victor.append(word_victor_mid)
    return word_victor


# doc_new_mid=split(doc)
# a=word_emb(doc_new_mid)

# a=fin(doc_new_mid)
# print(a[1])
# print(len(a[1]))
# print(len(a[1][0]))