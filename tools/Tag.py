# author:syt & monkeydc
# last edit time:

import pandas as pd
#import sys
import os
import numpy as np
import openpyxl


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

def countPMI(path):
    # 计算共现矩阵
    dict = generateDict(path)
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
    writeToExcel(file_path, metrix)


