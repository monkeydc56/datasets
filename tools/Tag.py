# author:syt & monkeydc
# last edit time:
import json
import pandas as pd
#import sys
import os
import numpy as np
import openpyxl
import math


os.chdir("C:/Users/哈哈/PycharmProjects/datasets")#地址修改成你自己的c盘那个，我暂时没改好这个，在看下代码
#生成格式化列表，可以用于共现计算
def generatelist(path):
    a = []
    with open(path, 'r') as f:
        for line in f:
            line = line.replace('[', '')
            line = line.replace(']', '')
            a.append(line.strip('\n').split("'"))
    b = []
    for i in range(len(a)):
        c = []
        for j in range(len(a[i])):
            if j % 2 == 1:
                c.append(a[i][j])
        b.append(c)
    return b

#建立字典
def generateDict(path,b1):
    a = []

    with open(path, 'r') as f:
        for line in f:
            line = line.replace('[', '')
            line = line.replace(']', '')
            a.append(line.strip('\n').split("'"))
    b = []
    for i in range(len(a)):
        # c = []
        for j in range(len(a[i])):
            if j % 2 == 1:
                # c.append(a[i][j])
                b.append(a[i][j])
    data_dict = pd.DataFrame(b)
    data_dict.columns = ['label']
    label_list = list(set(data_dict['label'].values.tolist()))
    labeldic = {}
    countdic = {}
    pos = 0

    for i in label_list:
        pos = pos + 1
        labeldic[i] = int(pos)
    #return labeldic
    appeardict = {}  # 各个标签为键，出现在哪些文本（将文本按顺序排列，出现的序号添加到列表中）为值，构造字典
    for l in label_list:
        appeardict[l]=[]
    i = 0
    for w in b1:
        for w1 in w:
            appeardict[w1].append(i)
        i += 1
    for m in label_list:
        countdic[m] = len(appeardict[m])
    return countdic,label_list#计算每个标签出现的次数用字典保存

# b = generatelist("./aapd/tag")
# label_list = generateDict("./aapd/tag",b)


def generateFMetrix(len):
    metrix = np.eye(len)
    return metrix

def countPMI(path):
    # 计算共现矩阵
    dict = generateDict(path,b)
    list = generatelist(path)
    length = len(dict)
    #metrix = generateFMetrix(length + 1)
    metrix = []#矩阵总是报错，因为盲猜矩阵固定了单元格内的数据格式，为能够保存中间结果使用list
    for i in range(length+1):
        metrix.append([])
        for j in range(length+1):
            metrix[i].append(0)

    for i in range(54):  # 字典里每一个词覆盖
        i += 1
        for j in range(54):
            j += 1
            z = 0
            for l in range(len(list)):  # 便利全部list
                for m in range(len(list[l])):  # 遍历list当中每一个可能，判断i是否在其中
                    if dict[i] == list[l][m]:
                        for n in range(len(list[l])):  # 遍历list当中每一个可能,判断j是否在其中，是则z加1
                            if dict[j] == list[l][n]:
                                z += 1
                            else:
                                pass
                    else:
                        pass
                # print(z)
            metrix[i][j] = z
    for i in range(length+1):
        if i ==0:
            metrix[i][i] = 0
        else:
            metrix[i][0] = dict[i]#给每一行每一列搭上标记
            metrix[0][i] = dict[i]#矩阵内部没办法打上string？总有报错说string没法convert in to float，所以不应该用这个方法存储
                                  #其实list可以考虑下，然后按照索引输出
    #没有计算完pmi，因为共现次数统计之后还需要
    return metrix

def writeToExcel(file_path, new_list):
    # total_list = [['A', 'B', 'C', 'D', 'E'], [1, 2, 4, 6, 8], [4, 6, 7, 9, 0], [2, 6, 4, 5, 8]]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = '明细'
    for r in range(len(new_list)):
        for c in range(len(new_list[0])):
            ws.cell(r + 1, c + 1).value = new_list[r][c]
            # excel中的行和列是从1开始计数的，所以需要+1
    wb.save(file_path)  # 注意，写入后一定要保存
    print("成功写入文件: " + file_path + " !")
    return None

da = pd.read_excel(r"C:\Users\哈哈\PycharmProjects\datasets\aapd\metrix.csv",index_col=0)#共现矩阵文件的路径
data=pd.read_table(r'C:\Users\哈哈\PycharmProjects\datasets\aapd\tag',header=None)#所有缩写标签的位置
data=data.values.tolist()
# tag = pd.read_csv(r"C:\Users\哈哈\PycharmProjects\datasets\aapd\datacsv.csv")#tag的csv文件路径
list = da.values.tolist()
list1 = da.values.tolist()

def newPMI(data,list,list1):#list和list1为共现矩阵的列表
    l = len(data)
    for i in range(len(list)):
        conx = list1[i][i]
        px = conx / l
        for j in range(len(list)):
            cony = list1[j][j]
            py = cony/l
            con = list1[i][j]
            pxy = con/l
            if con != 0:
                pmi = np.log(pxy / (px * py))
                list[i][j] = pmi
            else:
                list[i][j] = 0
    test = pd.DataFrame(data=list)
    test.to_csv(r"C:\Users\哈哈\PycharmProjects\datasets\aapd\pmi2.csv")  # 保存计算好的PMI

path = "D:\glove\.vector_cache\glove.6B.300d.txt"#glove路径
def Glove(path):
    embeddings_dict = {}
    embeddings_dict['<unk>']=np.zeros(300)#unk为300维的0
    with open(path,'r', encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
    return embeddings_dict

# # Calculate GloVe embeddings for each label in our target label subset.
TAG = pd.read_excel(r'C:\Users\哈哈\PycharmProjects\datasets\aapd\TAG.xlsx',header = None)#标签缩写与全称文件位置
def tra(TAG):
    label_LIST = []
    for i in range(len(TAG)):
        label_LIST.append(TAG.iloc[i, 1].replace('.', ' ').replace(', ',' ').lower())#将标签中的.去除,还需去除，含—觉得不需要去除
    return label_LIST

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
                sen_vec = sen_vec + embeddings_dict['<unk>']
            else:
                sen_vec = sen_vec + embeddings_dict[word]
                count += 1
                sen_vec /= count
        victor.append(sen_vec.tolist())
    return victor
#


def onehot(data,TAG):
    new=[]
    one_hot=[]
    for i in range(len(data)):
        new.append(data[i][0].replace('[','').replace(']','').replace("'",'').replace(',',' ').split())#分割为字符串
        one_hot_mid = [0] * len(TAG)
        for str in new[i]:#所有tag文件中的标签按行遍历
            hot = [0] * len(TAG)
            for j in range(len(TAG)):
                if str == TAG[0][j]:#缩写标签与对照表中的一样则所在的索引值为1
                    hot[j]=1
                else:
                    hot[j]=0
            one_hot_mid=[one_hot_mid[i]+hot[i] for i in range(min(len(one_hot_mid),len(hot)))]
        one_hot.append(one_hot_mid)


if __name__ == '__main__':
    metrix = countPMI('./aapd/tag')
    file_path = './results/metrix.csv'
    b=generatelist('./aapd/tag')
    label_list=generateDict('./aapd/tag',b)
    countdic=generateDict('./aapd/tag',b)
    #metrixP=PMI(metrix,countdic,label_list)
    #writeToExcel(file_path, metrix)