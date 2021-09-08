import numpy as np
import json
import pandas as pd

path = "D:\glove\.vector_cache\glove.6B.300d.txt"#glove路径

def Glove(path):
    embeddings_dict = {}
    embeddings_dict['<unk>']=np.zeros(300)
    with open(path,'r', encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector

    return embeddings_dict
#
# # Calculate GloVe embeddings for each label in our target label subset.
TAG = pd.read_excel(r'C:\Users\哈哈\PycharmProjects\datasets\aapd\TAG.xlsx',header = None)#标签全称对应位置
def tra(TAG):
    label_LIST = []
    for i in range(len(TAG)):
        label_LIST.append(TAG.iloc[i, 1].replace('.', ' ').replace(', ',' ').lower())#将标签中的.去除,还需去除，含—觉得不需要去除
    return label_LIST
#
#
#
# #对每个标签的所有词向量取均值，来生成一个平均的vector
def build_sentence_vector(label_LIST, size, embeddings_dict):
    sen_vec = np.zeros(size).reshape((1, size))
    new = []
    victor = []

    for i in range(len(label_LIST)):
        count = 0
        new.append(label_LIST[i].split())#吧每条标签的空格去除分为单个字符串
        for word in new[i]:
            if word not in embeddings_dict.keys():
                # embeddings_dict[word] = '<unk>'
                sen_vec = sen_vec + embeddings_dict['<unk>']
            else:
                sen_vec = sen_vec + embeddings_dict[word]

                count += 1
                sen_vec /= count
        victor.append(sen_vec.tolist())
    return victor
#
# label_LIST=tra(TAG)
# embeddings_dict=Glove(path)
# victors = build_sentence_vector(label_LIST, size=300, embeddings_dict=embeddings_dict)

# Save them for further use.
# glovepath = 'glow_label.json'
# with open(glovepath, 'w') as fp:
#     json.dump({'label_LIST':victors}, fp)
#     print("done")
data=pd.read_table(r'C:\Users\哈哈\PycharmProjects\datasets\aapd\tag',header=None)
data=data.values.tolist()

def onehot(data,TAG):
    new=[]
    one_hot=[]

    for i in range(len(data)):
        new.append(data[i][0].replace('[','').replace(']','').replace("'",'').replace(',',' ').split())#分割为字符串
        # count = 0
        one_hot_mid = [0] * len(TAG)
        for str in new[i]:#所有tag文件中的标签按行遍历
            # count+=1
        # print(count)
            hot = [0] * len(TAG)
            for j in range(len(TAG)):
                if str == TAG[0][j]:#缩写标签与对照表中的一样则所在的索引值为1
                    # hot = [0 for _ in range(len(TAG))]
                    hot[j]=1
                else:
                    hot[j]=0
            one_hot_mid=[one_hot_mid[i]+hot[i] for i in range(min(len(one_hot_mid),len(hot)))]
        one_hot.append(one_hot_mid)

    #     one_hot.append(hot)
    # return one_hot

a=onehot(data,TAG)
# print(a)


