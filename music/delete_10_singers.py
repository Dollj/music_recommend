import os

#删除歌曲少于10的歌手

def mkdir(path):
    '''
    判断文件夹是否存在，若不存在则创建它
    '''
    if os.path.exists(path)==False:
        os.makedirs(path)

def delete_10_singer(path,outpath):
    '''
    参数:
    ------------------------------
    path:str
         歌词文件路径，path='D:/Test/pycharmpjs/Lyrics_all/Lyrics/Lyrics/chinese/'
    outpath:str
         输出路径，outpath='D:/Lyrics_chinese/'
    ------------------------------
    输出:
    ------------------------------
    删除歌曲少于10的歌手
    ------------------------------
    '''
    file_list=os.listdir(path)  # file_list=['林俊杰'，'周杰伦'，...]
    for file_name in file_list:
        full_path=path+file_name+'/'
        full_name_list=os.listdir(full_path)  # full_name=['七里香.txt','发如雪.txt'，...]
        if len(full_name_list)>11:
            for full_name in full_name_list:
                full_name_path=full_path+full_name
                full_outpath=outpath+file_name+'/'
                mkdir(full_outpath)
                full_outpath_name=full_outpath+full_name
                #print(full_name_path)
                try:
                    with open(full_name_path,'r',encoding='utf-8') as fpr:
                        lyr=fpr.read()
                    print(lyr)
                    with open(full_outpath_name,'w',encoding='utf-8') as fpw:
                        fpw.write(lyr)
                except:
                    pass

if __name__ == "__main__":
    path='D:/lyrics_chinese_regu/'
    outpath='D:/lyrics_chinese_regu_regu/'
    delete_10_singer(path,outpath)


