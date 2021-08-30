import pandas as pd
from pandas import DataFrame


# data=pd.read_csv('shop.csv',sep='\t',header=0)
data = pd.read_csv('../aapd/datacsv.csv',sep=',',index_col=0)
data1 = data.sample(frac=0.7,replace=False)#flase是无放回的切割，有放回的切
#print(data1)
data1.to_csv('../aapd/train.csv',',')


data2 = data.sample(frac=0.3,replace=False)#flase是无放回的切割，有放回的切
#print(data2)
data2.to_csv('../aapd/test.csv',',')
