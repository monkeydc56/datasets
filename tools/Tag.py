# author:syt & monkeydc
# last edit time:

import pandas as pd
#import sys
import os
import numpy as np
import openpyxl
import math


os.chdir("C:/Users/哈哈/PycharmProjects/datasets")#地址修改成你自己的c盘那个，我暂时没改好这个，在看下代码
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


b = generatelist("./aapd/tag")
countdic = generateDict("./aapd/tag",b)
print(countdic)

def generateFMetrix(len):
    metrix = np.eye(len)
    return metrix

def PMI(metrix):
    for x,y in label_list:
        i=0
        j=0
        for i,j in range(55):
            if x == metrix[i][0] and y == metrix[0][j]:
                con=metrix[i][j]
                i += 1
                j += 1
        conx=countdic[x]
        cony=countdic[y]
        a = con / (conx * cony)
        pmi = np.log(a)
        metrixP=generateFMetrix(55)
        metrixP[0][1:]=label_list
        metrixP[1:][0]=label_list
        for p, q in range(55):
            if p == metrixP[i][0] and q == metrixP[0][j]:
                metrixP[p][q]=pmi
                p += 1
                q += 1
    return metrixP





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



if __name__ == '__main__':
    metrix = countPMI('./aapd/tag')
    file_path = './results/metrix.csv'
    b=generatelist('./aapd/tag')
    label_list=generateDict('./aapd/tag',b)
    countdic=generateDict('./aapd/tag',b)
    print(countdic)
    #metrixP=PMI(metrix,countdic,label_list)
    #writeToExcel(file_path, metrix)