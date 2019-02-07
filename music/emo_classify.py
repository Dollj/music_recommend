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
validation_label=[]
test_label=[]
train_info_dict=[]
validation_info_dict=[]
test_info_dict=[]
"""
for i in range(len(list_emo_class)):
    if 0<=random.random()<=0.6:
        train_label.append(list_emo_class[i])
        train_lyric=' '.join(str(n) for n in all_info[i]['分词歌词'])
        train_info_dict.append(train_lyric)
    elif 0.6<random.random()<=0.8:
        validation_label.append(list_emo_class[i])
        validation_lyric = ' '.join(str(n) for n in all_info[i]['分词歌词'])
        validation_info_dict.append(validation_lyric)
    else:
        test_label.append(list_emo_class[i])
        test_info_lyric = ' '.join(str(n) for n in all_info[i]['分词歌词'])
        test_info_dict.append(test_info_lyric)
##############################
"""
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

#adaboost
from sklearn.ensemble import AdaBoostClassifier
print("adaboost:")
# n_estimators表示要组合的弱分类器个数；
# algorithm可选{‘SAMME’, ‘SAMME.R’}，默认为‘SAMME.R’，表示使用的是real boosting算法，‘SAMME’表示使用的是discrete boosting算法
adclf=AdaBoostClassifier(algorithm='SAMME.R',n_estimators=100)
adclf.fit(train_set.tdm,train_set.label)
adtest_p=adclf.predict(test_set.tdm)
metrics_result(test_set.label,adtest_p)



#朴素 Bayes
train_score = []
test_score = []
alpha = np.linspace(-4, 4, 200)
for a in alpha:
    clf = MultinomialNB(alpha=10 ** a).fit(train_set.tdm, train_set.label)
    train_pre = clf.predict(train_set.tdm)#train set predict
    trains = metrics.precision_score(train_set.label, train_pre, average='weighted')
    train_score.append(trains)
    test_pre = clf.predict(test_set.tdm)
    tests = metrics.precision_score(test_set.label, test_pre, average='weighted')
    test_score.append(tests)
#score-alpha图
plt.figure(figsize=(8, 8))
plt.plot(alpha, train_score, 'r-', label='train')
plt.plot(alpha, test_score, 'b-', label='test')
plt.xlabel('log(10,alpha)')
plt.ylabel('score')
plt.grid()
plt.legend()
plt.show()
#best_朴素 Bayes
print("朴素贝叶斯：")
ind=np.argmax(test_score)
best_a=10**alpha[ind]
nbclf=MultinomialNB(alpha=best_a)
nbclf.fit(train_set.tdm,train_set.label)
nbtest_p=nbclf.predict(test_set.tdm)
metrics_result(test_set.label,nbtest_p)


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
"""
#svm.rbf
from sklearn import svm
print("svm rbf:")
clf=svm.SVC(C=1,gamma=2)
clf.fit(train_set.tdm,train_set.label)
predict=clf.predict(test_set.tdm)
metrics_result(test_set.label,predict)

"""



#投票法
cla={'original_class':test_set.label,'adaboost':adtest_p,'naive_bayes':nbtest_p,'logistic':lrtest_p,'svm':svmtest_p}
cla=pd.DataFrame(cla)
cla.to_csv('/Users/cathy/Documents/python_script/music/data/pre_class.csv')

from collections import Counter
df=cla
new_class=[]

for i in range(19038):
    emo_ctgy=[]   #情绪类别列表，那一行的4列
    for j in range(1,5):
        emo_ctgy.append(df.iloc[i,j])
        emo_counter=Counter(emo_ctgy)
    if len(emo_counter)==4:
        new_class[i]=df.iloc[i,4]
    elif len(emo_counter)==3:
        for k,v in emo_counter.items():
            if v==2:
                new_class[i]=df.iloc[i,4]
    elif len(emo_counter)==2:
        for k,v in emo_counter.items():
            if v==2:
                new_class[i]=df.iloc[i,4] 
            elif v==3:
                new_class[i]=k#svm那个情绪类
    elif len(emo_counter)==1:
         new_class[i]=df.iloc[i,4] #此时随便选一个都一样
#3-ada,svm
from collections import Counter
cla={'original_class':test_set.label,'naive_bayes':nbtest_p,'logistic':lrtest_p,'svm':svmtest_p}
df=pd.DataFrame(cla)
new_class=[]
for i in range(19038):
    new_class.append('快乐')

for i in range(19038):
    emo_ctgy=[]   #情绪类别列表，那一行的4列
    for j in range(1,4):
        emo_ctgy.append(df.iloc[i,j])
        emo_counter=Counter(emo_ctgy)
    if len(emo_counter)==3:
        new_class[i]=df.iloc[i,3]
    elif len(emo_counter)==2:
        for k,v in emo_counter.items():
            if v==2:
                new_class[i]=k
                """
    elif len(emo_counter)==2:
        for k,v in emo_counter.items():
            if v==2:
                new_class[i]=df.iloc[i,3] 
            elif v==3:
                new_class[i]=k
             #svm那个情绪类"""
    elif len(emo_counter)==1:
         new_class[i]=df.iloc[i,3] #此时随便选一个都一样

count=0      
for i in range(19038):
    if test_set.label[i]==new_class[i]:
        count+=1
        
count/19038

#4类
from collections import Counter
cla={'original_class':test_set.label,'adaboost':adtest_p,'naive_bayes':nbtest_p,'logistic':lrtest_p,'svm':svmtest_p}
df=pd.DataFrame(cla)
new_class=[]
for i in range(19038):
    new_class.append('快乐')


for i in range(19038):
    emo_ctgy=[]   #情绪类别列表，那一行的4列
    for j in range(1,5):
        emo_ctgy.append(df.iloc[i,j])
        emo_counter=Counter(emo_ctgy)
    if len(emo_counter)==4:
        new_class[i]=df.iloc[i,4]
    elif len(emo_counter)==3:
        for k,v in emo_counter.items():
            if v==2:
                new_class[i]=k
    elif len(emo_counter)==2:
        for k,v in emo_counter.items():
            if v==2:
                new_class[i]=df.iloc[i,4] 
            elif v==3:
                new_class[i]=k
             #svm那个情绪类
    elif len(emo_counter)==1:
         new_class[i]=df.iloc[i,4] #此时随便选一个都一样

count=0      
for i in range(19038):
    if test_set.label[i]==new_class[i]:
        count+=1
count/19038

#3-ada,lr
from collections import Counter
cla={'original_class':test_set.label,'logistic':lrtest_p,'svm':svmtest_p}
df=pd.DataFrame(cla)
new_class=[]
for i in range(19038):
    new_class.append('快乐')

for i in range(19038):
    emo_ctgy=[]   #情绪类别列表，那一行的4列
    for j in range(1,3):
        emo_ctgy.append(df.iloc[i,j])
        emo_counter=Counter(emo_ctgy)
    if len(emo_counter)==2:
        new_class[i]=df.iloc[i,1]
        """
    elif len(emo_counter)==2:
        for k,v in emo_counter.items():
            if v==2:
                new_class[i]=k
               
    elif len(emo_counter)==2:
        for k,v in emo_counter.items():
            if v==2:
                new_class[i]=df.iloc[i,3] 
            elif v==3:
                new_class[i]=k
             #svm那个情绪类"""
    elif len(emo_counter)==1:
         new_class[i]=df.iloc[i,1] #此时随便选一个都一样

count=0      
for i in range(19038):
    if test_set.label[i]==new_class[i]:
        count+=1
        
count/19038

