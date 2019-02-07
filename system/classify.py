# -*- coding:utf-8
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
import json,jieba




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



def lr(test):
    excelFile = r"/Users/cathy/Documents/研究生/文本挖掘/music/data/emotion2.csv"
    df = pd.read_csv(open(excelFile, encoding='gbk'))

    with open('/Users/cathy/Documents/研究生/文本挖掘/music/data/chinese_seg.json', 'r', encoding='gbk') as fp:
        all_info = json.load(fp)

    def all_list(arr):
        result = {}
        for i in set(arr):
            result[i] = arr.count(i)
        return result

    list_emo_class = list(df['emotion_class'])

    #logistic regression
    # 训练集train，验证集validation，测试集test
    train_label = []
    train_info_dict = []
    test_info_dict = []
    n = len(list_emo_class)
    point = int((n * 0.8))
    for i in range(point):
        train_label.append(list_emo_class[i])
        train_lyric = ' '.join(str(n) for n in all_info[i]['分词歌词'])
        train_info_dict.append(train_lyric)
    test_label='快乐'
    test_cut=jieba.cut(test)
    test_info_lyric = ' '.join(str(n) for n in test_cut)
    test_info_dict.append(test_info_lyric)
    # train_set, test_set = v_space(train_label,validation_label,train_info_dict,validation_info_dict)
    train_set, test_set = v_space(train_label, test_label, train_info_dict, test_info_dict)

    print("logistic regression：")
    from sklearn import linear_model
    lrclf=linear_model.LogisticRegression()
    lrclf.fit(train_set.tdm,train_set.label)
    lrtest_p=lrclf.predict(test_set.tdm)
    return lrtest_p


