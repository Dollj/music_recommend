# -*- coding:utf-8
import pandas as pd
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


excelFile=r"D:/emotion2.csv"#21类 emotion_class
df=pd.read_csv(open(excelFile,encoding='gbk'))
list_emo_class=list(df['emotion_class'])

with open('D:/chinese_seg.json','r',encoding='gbk') as fp:
    all_info=json.load(fp)

s = {k: list() for x in all_info for k, v in x.items()}
[s[k].append(v) for x in all_info for k, v in x.items()]
info={k: list(v) for k, v in s.items()}
"""
lyric=[]
for i in range(len(list_emo_class)):
    l=' '.join(str(n) for n in info['分词歌词'][i])
    lyric.append(l)
"""

c={"emo_class":list_emo_class,"seg_lyric":info['分词歌词']}
label_content=pd.DataFrame(c)
label_content=label_content.set_index('emo_class')


happy_data=label_content.ix['快乐',]
romantic_data=label_content.ix['甜蜜',]
encourage_data=label_content.ix['励志',]
heal_data=label_content.ix['治愈',]
angry_data=label_content.ix['宣泄',]
sad_data=label_content.ix['伤感',]

sad_lyric=[]
for i in range(len(sad_data)):
    sad_lyric.extend(sad_data.ix[i,'seg_lyric'])
sad_lyric=' '.join(sad_lyric)

color_mask = plt.imread("D:/2.jpg")
def make_worldcloud(wl_space_split):
    # text_from_file_with_apath = open(file_path, 'r').read()
    # wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all=False)
    # wl_space_split = " ".join(wordlist_after_jieba)
    # print wl_space_split
    backgroud_Image=color_mask

    '''设置词云样式'''
    # stopwords = STOPWORDS.copy()
    # stopwords.add("真的") #可以加多个屏蔽词
    wc = WordCloud(
        width=1024,
        height=768,
        background_color='white',# 设置背景颜色
        mask=backgroud_Image,# 设置背景图片
        font_path='C:/Users/xn/Downloads/yahei.ttf',  # 设置中文字体，若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
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

make_worldcloud(sad_lyric)