import os
import re

def mkdir(path):#####判断文件夹是否存在，若不存在则创建它
    if os.path.exists(path)==False:
        os.makedirs(path)

path='D:/Lyrics_chinese/'
path1='D:/lyrics_chinese_regu/'
file_list=os.listdir(path)#['宋东野',....]

for file_name in file_list:
    full_path=path+file_name+'/'#'D:/lyrics1/folk/宋东野/'
    full_path1=path1+file_name+'/'
    mkdir(full_path1)
    song_list=os.listdir(full_path)#['安和桥.txt',...]
    song_regular_list=[]
    for song in song_list:
        song_regular=re.sub("[\)\(]",'',song)
        song_regular=re.sub('[（）]', '', song_regular)
        song_regular=re.sub('[\s\.-]','',song_regular)
        song_regular=re.sub("[a-zA-z]", '', song_regular)
        if len(song_regular)>0:
            song_regular_list.append(song_regular)
        else:
            song_regular_list.append(song)
    song_regular_set=set(song_regular_list)
    print(song_regular_set)
    for i in song_list:
        for j in song_regular_set:
            if j in i:
                full_name=full_path+i
                with open(full_name,'r',encoding='utf-8') as fp:
                    lyric=fp.read()
                full_name1=full_path1+j+'.txt'
                with open(full_name1,'w',encoding='utf-8') as fp1:
                    fp1.write(lyric)