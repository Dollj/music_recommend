#-*-coding:utf-8-*-
import os
import re
import json
import pyltp
from pyltp import Segmentor

model_path='D:/LTP/ltp_data_v3.4.0/ltp_data_v3.4.0/cws.model'
noise=['作曲','作词','编曲','制作人','吉他','贝斯','鼓','录音师','混音师','插画','Drums','Arragement','Programing','Bass','Guitars','Recording','演唱者','编辑','歌词:','歌词：']###不想要的信息
information=['作词','作曲']#####歌曲信息

def stopwordslist(filepath):  # 读取停用词
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

def mkdir(path):#####判断文件夹是否存在，若不存在则创建它
    if os.path.exists(path)==False:
        os.makedirs(path)

#path=D:/lyrics1/folk_regular/
#输出路径：outpath=D:/lyrics1/folk_seg/
def folkseg(path,outpath):
    segmentor = Segmentor()
    segmentor.load(model_path)
    file_list=os.listdir(path)###['赵照'，'赵雷',...]
    song_info_all=[]######所有歌曲信息
    for file_name in file_list:
        full_path=path+file_name+'/'##D:/lyrics1/folk_regular/赵照/
        song_name_list=os.listdir(full_path)#####['1980年代的爱情.txt',...]
        for song_name in song_name_list:
            song_info={}####一首歌的信息
            song_info["歌手"]=song_info.get("歌手",file_name)
            song_info["歌名"]=song_info.get("歌名",song_name)
            full_name=full_path+song_name#####歌词的全部路径
            with open(full_name,'r',encoding="utf-8") as fp:
                data=fp.readlines()

            for line in data:
                for i in information:####获取歌曲信息
                    if i in line:
                        line1=line.strip()
                        line1=line1.replace(' ','')
                        line1=line1.replace(i+':','')
                        song_info[i]=song_info.get(i,line1)

            lyric=''
            for line in data:#每行
                mark=0
                for i in noise:
                    if i in line:
                        mark=mark+1
                if mark<1:
                    line=line.strip()####去除这一行首位的空字符和换行
                    line=re.sub('^.+?:','',line)
                    line=re.sub('\(.*?\)','',line)
                    line=re.sub('（.*?）','',line)
                    pattern=re.compile(r"[\u4e00-\u9fa5]")  # 匹配中文
                    line=''.join(re.findall(pattern,line))
                    lyric=lyric+line####把每行拼接在一起
            lyric=segmentor.segment(lyric)####对一整首歌进行分词
            lyric_seg=','.join(lyric)######转写成以，分割的字符串
            print(lyric_seg)
            lyric_seg_list=lyric_seg.split(',')
            lyric_seg_list_stopwords=[]#去停用词后的歌词
            for i in lyric_seg_list:
                if i not in stopwords:
                    lyric_seg_list_stopwords.append(i)
            song_info["分词歌词"]=song_info.get("分词歌词",lyric_seg_list_stopwords)

            with open(full_name,'r',encoding="utf-8") as fp:
                data=fp.readlines()
            song_info["原歌词"]=song_info.get("原歌词",data)
            song_info_all.append(song_info)
            print(song_info)
    out_name=outpath+'folk.json'
    with open(out_name,'w',encoding='utf-8') as fp:
        json.dump(song_info_all,fp)

if __name__ == "__main__":
    path='D:/lyrics_chinese_regu_regu/'
    outpath='D:/lyrics_chinese_regu_regu_seg/'
    stopwords=stopwordslist('C:/Users/xiaoming/Desktop/stopwords.txt')  # 这里加载停用词的路径
    folkseg(path,outpath)