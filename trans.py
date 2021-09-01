import pandas as pd

TAG = pd.read_excel(r'C:\Users\哈哈\PycharmProjects\datasets\aapd\TAG.xlsx',header = None)#标签全称对应位置
tag = pd.read_table(r'C:\Users\哈哈\PycharmProjects\datasets\aapd\tag',header = None)#标签文件位置

# print(TAG.shape)
#print(TAG.head())
TAG = TAG.set_index(0, True)
print(TAG)
# print(TAG.head())
def transfor(tag,TAG):
    for j in range(tag.shape[0]):
        list1 = tag.iloc[j, 0][1:-1].split(', ')#吧tag文件内容切分
        list2 = []
        for str in list1:
            list2.append(TAG.loc[str[1:-1]].values[0])#根据字符串索引值，再返回字符串添加进列表
        #rint(list2)
        tag.iloc[j, 0] = (', '.join(list2))

    tag.to_csv(r"C:\Users\哈哈\PycharmProjects\datasets\aapd\newtag.csv")  # 保存计算好的PMI
    print('done')

transfor(tag,TAG)