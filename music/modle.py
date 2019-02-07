# -*- coding:utf-8
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
import json,random
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt


excelFile=r"/Users/cathy/Documents/python_script/music/data/emotion2.csv"
df=pd.read_csv(open(excelFile,encoding='gbk'))


with open('/Users/cathy/Documents/python_script/music/data/chinese_seg.json','r',encoding='gbk') as fp:
    all_info=json.load(fp)


def all_list(arr):
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result


list_emo_class=list(df['emotion_class'])
print("各情感统计：")
print(all_list(list_emo_class))#各情感统计

#每首歌label-content(segment)
def data2bunch(tolabel,tolyric):
    bunch = Bunch(label=[], content=[])
    bunch.label.extend(tolabel)
    bunch.content.extend(tolyric)
    return bunch


#.._emoclass集合的label,.._info列表字典信息
def v_space(train_emoclass,test_emoclass,train_info, test_info):
    train_bunch = data2bunch(train_emoclass,train_info)
    # tdm，tf-idf权重矩阵，tdm(i,j)第j个词在第i类别的权重，tf-idf值
    # vocabulary是单词和单词对应的序号，词向量空间坐标
    # sublinear_tf，1+log(tf)计算tdm词频矩阵,max_df某词在所有类别中占的比重最高不能超过0.5
    trainb_tfidf = Bunch(label=train_bunch.label, content=train_bunch.content, tdm=[], vocabulary={})
    vectorizer1 = TfidfVectorizer(sublinear_tf=True, max_df=0.5)
    trainb_tfidf.tdm = vectorizer1.fit_transform(train_bunch.content)
    trainb_tfidf.vocabulary = vectorizer1.vocabulary_

    test_bunch = data2bunch(test_emoclass,test_info)
    testb_tfidf = Bunch(label=test_bunch.label, content=test_bunch.content, tdm=[], vocabulary=trainb_tfidf.vocabulary)
    vectorizer2 = TfidfVectorizer(sublinear_tf=True, max_df=0.5, vocabulary=trainb_tfidf.vocabulary)
    testb_tfidf.tdm = vectorizer2.fit_transform(test_bunch.content)

    return (trainb_tfidf, testb_tfidf)


#训练集train，验证集validation，测试集test
train_label=[]
test_label=[]
train_info_dict=[]
test_info_dict=[]
n=len(list_emo_class)
point=int((n*0.8))
for i in range(point):
    train_label.append(list_emo_class[i])
    train_lyric=' '.join(str(n) for n in all_info[i]['分词歌词'])
    train_info_dict.append(train_lyric)
for j in range(point,(n-1)):
    test_label.append(list_emo_class[j])
    test_info_lyric = ' '.join(str(n) for n in all_info[j]['分词歌词'])
    test_info_dict.append(test_info_lyric)
#train_set, test_set = v_space(train_label,validation_label,train_info_dict,validation_info_dict)
train_set, test_set = v_space(train_label,test_label,train_info_dict,test_info_dict)


#模型评估
def metrics_result(actual, pre):
    testscore = metrics.precision_score(actual, pre, average='weighted')
    print("精度：", testscore)
    testscore1 = metrics.recall_score(actual, pre, average='weighted')
    print("召回：", testscore1)
    testscore2 = metrics.f1_score(actual, pre, average='weighted')
    print("f1-score:", testscore2)

#logistic regression
print("logistic regression：")
from sklearn import linear_model
lrclf=linear_model.LogisticRegression()
lrclf.fit(train_set.tdm,train_set.label)
lrtest_p=lrclf.predict(test_set.tdm)
metrics_result(test_set.label,lrtest_p)

#svm
from sklearn import svm
print("svm:")
clf=svm.SVC(C=0.8,kernel='linear',decision_function_shape='over')
clf.fit(train_set.tdm,train_set.label)
svmtest_p=clf.predict(test_set.tdm)
metrics_result(test_set.label,svmtest_p)

""""
#随机森林
s = {k: list() for x in all_info for k, v in x.items()}
[s[k].append(v) for x in all_info for k, v in x.items()]
info={k: list(v) for k, v in s.items()}
lyric=[]
for i in range(len(list_emo_class)):
    l=' '.join(str(n) for n in info['分词歌词'][i])
    lyric.append(l)


c={"emo_class":list_emo_class,"seg_lyric":lyric}
label_content=pd.DataFrame(c)
label_content=label_content.set_index('emo_class')


happy_data=label_content.ix['快乐']
romantic_data=label_content.ix['甜蜜',]
encourage_data=label_content.ix['励志',]
heal_data=label_content.ix['治愈',]
angry_data=label_content.ix['宣泄',]
sad_data=label_content.ix['伤感',]

happy_data_1=happy_data[0:10000]
romantic_data_1=romantic_data[0:10000]
encourage_data_1=encourage_data[0:10000]
heal_data_1=heal_data[0:10000]
angry_data_1=angry_data[0:10000]
sad_data_1=sad_data[0:10000]
#"emo_class","seg_lyric"
train_dict=[happy_data_1[0:8000],romantic_data_1[0:8000],encourage_data_1[0:8000],heal_data_1[0:8000],angry_data_1[0:8000],sad_data_1[0:8000]]
train_data=pd.concat(train_dict)

test_dict=[happy_data_1[8000:10000],romantic_data_1[8000:10000],encourage_data_1[8000:10000],heal_data_1[8000:10000],angry_data_1[8000:10000],sad_data_1[8000:10000]]
test_data=pd.concat(test_dict)

rftrain_label=[]
rftrain_info=[]
rftest_label=[]
rftest_info=[]
for i in range(8000*4):
    rftrain_label.append(train_data.ix[[i]].index.values[0])
    train_lyric=train_data.ix[i,'seg_lyric']
    rftrain_info.append(train_lyric)
for j in range(2000*4):
    rftest_label.append(test_data.ix[[j]].index.values[0])
    test_lyric = test_data.ix[j,'seg_lyric']
    rftest_info.append(test_lyric)
#train_set, test_set = v_space(train_label,validation_label,train_info_dict,validation_info_dict)
train_set, test_set = v_space(rftrain_label,rftest_label,rftrain_info,rftest_info)


from sklearn.ensemble import RandomForestClassifier
print("random forest:")
rfclf=RandomForestClassifier(n_estimators=50,max_depth=None)
rfclf.fit(train_set.tdm,train_set.label)
rftest_p=rfclf.predict(test_set.tdm)
metrics_result(test_set.label,rftest_p)


"""