import pandas as pd
from pandas import DataFrame
import json
from numpy import *

with open('D:/lyrics_chinese_regu_regu_seg/chinese_seg.json','r',encoding='utf-8') as fp:
    graph=json.load(fp)

#子类-父类，find父类的key
def Emo_FineToCrude(subdiv):
    Div_dict={'PA':'PA','PE':'PE','PD':'PD','PH':'PH','PG':'PG','PB':'PB','PK':'PK','NA':'NA','NB':'NB','NJ':'NJ','NH':'NH','PH':'PH','NI':'NI','NC':'NC','NG':'NG','NE':'NE','ND':'ND','NN':'NN','NK':'NK','NL':'NL','PC':'PC'}
    result=[k for k,v in Div_dict.items() if subdiv in v]
    return result


excelFile="D:/情感词汇本体/情感词汇本体.xlsx"
df=pd.read_excel(excelFile)
#print(df[:10])
emo_class_dict=dict(zip(df['词语'],df['情感分类']))
emotion= pd.DataFrame(zeros([len(graph),21]),columns=['PA', 'PE', 'PD', 'PH', 'PG', 'PB', 'PK', 'NA', 'NB', 'NJ', 'NH', 'NI', 'NC', 'NG', 'NE', 'ND', 'NN', 'NK', 'NL', 'PC'])
print(len(graph))
for g in range(len(graph)):#每首歌循环
    lyric_song=graph[g]['分词歌词']#每首歌分词后歌词（列表）
    n=len(lyric_song)#一首歌歌词分词后长度
    for k in range(n):
        for word in df['词语']:
            if lyric_song[k]==word:
                ParentClass=Emo_FineToCrude(emo_class_dict[word])
                emotion.loc[g,ParentClass] += 1
            else:
                continue
emotion.to_csv('D:/emotion.csv')