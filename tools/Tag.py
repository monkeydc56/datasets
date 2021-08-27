import pandas as pd
#import sys
import os
import numpy as np

os.chdir("/Users/xiexingyu/PycharmProjects/datasets")#地址修改成你自己的c盘那个，我暂时没改好这个，在看下代码
#print(os.getcwd())
#sys.path.append()

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
def generateDict(path):
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
    pos = 0
    for i in label_list:
        pos = pos + 1
        labeldic[pos] = str(i)
    return labeldic

def generateFMetrix(len):
    metrix = np.eye(len)
    return metrix


#计算共现矩阵
dict = generateDict('./aapd/tag')
list = generatelist('./aapd/tag')
length = len(dict)
metrix = generateFMetrix(length)
