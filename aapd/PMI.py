import pandas as pd
import numpy as np
data = pd.read_excel(r"C:\Users\哈哈\PycharmProjects\datasets\aapd\metrix.csv",index_col=0)#共现矩阵文件的路径
list=data.values.tolist()
#print(list[0][0])
#print(data)
#print(list[1][1])

def PMI(data):
    i = 0
    j = 0
    list1 = data.columns.tolist()
    list2 = data.index.tolist()
    for i in range(54):
        for j in range(54):
            conx = countdic[list1[i]]
            cony = countdic[list2[j]]
            con = data.iloc[i, j]

            # conx=countdic[x]

            a = con / (conx * cony)
            pmi = np.log(a)
            data.iloc[i, j] = pmi

    # metrixP=generateFMetrix(54)
    # metrixP[0][1:]=label_list
    # metrixP[1:][0]=label_list
    #pd.to_csv(r"C:\Users\哈哈\PycharmProjects\datasets\aapd\pmicsv.csv")#保存计算好的PMI
    #print(data)
    # return metrixP

def newPMI(data,list):
    i = 0
    l = len(data)
    for i in range(len(list)):
        conx = list[i][i]
        px = conx/l
        i += 1
        j = 0
        for j in range(len(list)):
            cony = list[j][j]
            py = cony/l
            con = list[i][j]
            pxy = con/l
            j += 1

            #print(con)


            if con == 0:
                pmi=0
                print("b")
            else:
                #pmi = np.log(pxy / (px * py))
                #list[i][j] = pmi
    #print("a")
    #pd.to_csv(r"C:\Users\哈哈\PycharmProjects\datasets\aapd\newpmicsv.csv")  # 保存计算好的PMI

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


# 建立字典
def generateDict(path, b1):
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
    # return labeldic
    appeardict = {}  # 各个标签为键，出现在哪些文本（将文本按顺序排列，出现的序号添加到列表中）为值，构造字典
    for l in label_list:
        appeardict[l] = []
    i = 0
    for w in b1:
        for w1 in w:
            appeardict[w1].append(i)
        i += 1
    for m in label_list:
        countdic[m] = len(appeardict[m])
    print(len(countdic))
    return countdic, label_list  # 计算每个标签出现的次数用字典保存


#b = generatelist("./aapd/tag")
#countdic, label_list = generateDict("./aapd/tag", b)
#print(countdic)


c = newPMI(data,list)


