# -*- coding:utf-8
import pandas as pd
from pandas import DataFrame
import numpy as np
import json,random

excelFile=r"/Users/cathy/Documents/研究生/文本挖掘/music/data/emotion2.csv"#Unnamed: 0	快乐	治愈	思念	伤感	浪漫	愤慨	忐忑	max_value	emotion_class
df=pd.read_csv(open(excelFile,encoding='gbk'))
#list_emo_class=list(df['emotion_class'])

with open('/Users/cathy/Documents/研究生/文本挖掘/music/data/chinese_seg.json','r',encoding='gbk') as fp:
    all_info=json.load(fp)


#字典型列表转成数据框
s = {k: list() for x in all_info for k, v in x.items()}
[s[k].append(v) for x in all_info for k, v in x.items()]
info={k: list(v) for k, v in s.items()}
cut_txt_name=[i.replace('.txt','') for i in info['歌名']]

#歌名中带.txt
table={"singer":info["歌手"],"song":cut_txt_name,"类别":list(df['emotion_class'])}
table=pd.DataFrame(table)
table=table.set_index('类别')
table_romantic=table.ix['甜蜜',]
table_happy=table.ix['快乐',]
table_encourage=table.ix['励志',]
table_heal=table.ix['治愈',]
table_angry=table.ix['宣泄',]
table_sad=table.ix['伤感',]


n_romantic=len(table_romantic)
n_happy=len(table_happy)
n_encourage=len(table_encourage)
n_heal=len(table_heal)
n_angry=len(table_angry)
n_sad=len(table_sad)

#random number
random_romantic = random.sample(range(0,n_romantic),50)
random_happy=random.sample(range(0,n_happy),50)
random_encourage=random.sample(range(0,n_encourage),50)
random_heal=random.sample(range(0,n_heal),50)
random_angry=random.sample(range(0,n_angry),50)
random_sad=random.sample(range(0,n_sad),50)

def romantic():
    table_romantic_data=table_romantic.iloc[random_romantic,:]
    table_romantic_input = []
    for i in range(50):
        s = {}
        s['id'] = i + 1
        s['singer'] = table_romantic_data.ix[i, 'singer']
        s['song'] = table_romantic_data.ix[i, 'song']
        table_romantic_input.append(s)
    return table_romantic_input

def happy():
    table_happy_data=table_happy.iloc[random_happy,:]
    #print(table_happy_data.ix[0,'singer'])
    table_happy_input=[]
    for i in range(50):
        s={}
        s['id']=i+1
        s['singer']=table_happy_data.ix[i,'singer']
        s['song']=table_happy_data.ix[i,'song']
        table_happy_input.append(s)
    return table_happy_input

def encourage():
    table_encourage_data=table_encourage.iloc[random_encourage,:]
    table_encourage_input = []
    for i in range(50):
        s = {}
        s['id'] = i + 1
        s['singer'] = table_encourage_data.ix[i, 'singer']
        s['song'] = table_encourage_data.ix[i, 'song']
        table_encourage_input.append(s)
    return  table_encourage_input

def heal():
    table_heal_data=table_heal.iloc[random_happy,:]
    table_heal_input = []
    for i in range(50):
        s = {}
        s['id'] = i + 1
        s['singer'] = table_heal_data.ix[i, 'singer']
        s['song'] = table_heal_data.ix[i, 'song']
        table_heal_input.append(s)
    return table_heal_input

def angry():
    table_angry_data=table_angry.iloc[random_angry,:]
    table_angry_input = []
    for i in range(50):
        s = {}
        s['id'] = i + 1
        s['singer'] = table_angry_data.ix[i, 'singer']
        s['song'] = table_angry_data.ix[i, 'song']
        table_angry_input.append(s)
    return table_angry_input

def sad():
    table_sad_data=table_sad.iloc[random_sad,:]
    table_sad_input = []
    for i in range(50):
        s = {}
        s['id'] = i + 1
        s['singer'] = table_sad_data.ix[i, 'singer']
        s['song'] = table_sad_data.ix[i, 'song']
        table_sad_input.append(s)
    return table_sad_input

"""
import hashlib
# 1.创建一个hash对象
h = hashlib.sha256()
# 2.填充要加密的数据
passwordstr = 'srtv4'
h.update(bytes(passwordstr, encoding='utf-8'))
# 3.获取加密结果
pawd_result = h.hexdigest()
print(pawd_result)
"""
"""
if __name__ == "__main__":
    happy_list=happy()
    print(happy_list)
"""