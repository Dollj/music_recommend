import os

#去除空歌词文件
def emperty_file(path):
    '''
    参数:
    -------------------------
    path:str
        歌词文件路径，path='D:/Test/pycharmpjs/Lyrics_all/Lyrics/Lyrics/chinese/'
    -------------------------
    输出;
    -------------------------
    把每个歌手的空歌词文件和无歌词文件删除
    -------------------------
    '''
    file_list=os.listdir(path)  # file_list=['林俊杰'，'周杰伦'，...]
    for file_name in file_list:
        full_path=path+file_name+'/'
        full_name_list=os.listdir(full_path)  # full_name=['七里香.txt','发如雪.txt'，...]
        for full_name in full_name_list:
            full_name_path=full_path+full_name  # 'D:/Test/pycharmpjs/Lyrics_all/Lyrics/Lyrics/chinese/周杰伦/七里香.txt'
            if os.path.getsize(full_name_path)<60:
                os.remove(full_name_path)

if __name__ == "__main__":
    path='D:/lyrics_chinese_regu/'
    emperty_file(path)