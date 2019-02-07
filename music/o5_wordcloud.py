# -*- coding: utf-8 -*-
import re
from os import path
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

d = path.dirname(__file__)
stopwords_path = 'result/stopwords.txt' # 停用词词表

def jiebaclearText(text_path):
    # text_path = 'E:/python/weibo_analysis/result/1774994513'
    text = open(path.join(d, text_path)).read()
    text = re.sub("[0-9]", "", text)
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    f_stop = open(stopwords_path)
    try:
        f_stop_text = f_stop.read( )
        f_stop_text=unicode(f_stop_text,'utf-8')
    finally:
        f_stop.close( )
    f_stop_seg_list=f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    return ''.join(mywordlist)


def make_worldcloud(wl_space_split):
    # text_from_file_with_apath = open(file_path, 'r').read()
    # wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=False)
    # wl_space_split = " ".join(wordlist_after_jieba)
    # print wl_space_split
    backgroud_Image = plt.imread('E:/python/weibo_analysis/result/muban.jpg')
    print u'加载图片成功！'
    '''设置词云样式'''
    # stopwords = STOPWORDS.copy()
    # stopwords.add("真的") #可以加多个屏蔽词
    wc = WordCloud(
        width=1024,
        height=768,
        background_color='white',# 设置背景颜色
        mask=backgroud_Image,# 设置背景图片
        font_path='E:/python/weibo_analysis/result/ziti.ttf',  # 设置中文字体，若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
        max_words=200, # 设置最大现实的字数
        # stopwords=stopwords,# 设置停用词
        max_font_size=300,# 设置字体最大值
        random_state=50,# 设置有多少种随机生成状态，即有多少种配色方案
    )
    wc.generate_from_text(wl_space_split)#开始加载文本
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)#字体颜色为背景图片的颜色
    plt.imshow(wc)# 显示词云图
    plt.axis('off')# 是否显示x轴、y轴下标
    plt.show()#显示
    # 获得模块所在的路径的
    d = path.dirname(__file__)
    # os.path.join()：  将多个路径组合后返回
    wc.to_file(path.join(d, "pic.jpg"))
    print u'生成词云成功!'


text1 = jiebaclearText( 'E:/python/weibo_analysis/result/1774994513')
print text1
make_worldcloud(text1)
