# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 20:37:18 2018

@author: xiaoming
"""
import requests
import json
import re
import os
from bs4 import BeautifulSoup

with open('D:/singer_id.json','r',encoding='utf-8') as fp:
    singer_info=json.load(fp)#####歌手信息

def mkdir(path):#####判断文件夹是否存在，若不存在则创建它
    if os.path.exists(path)==False:
        os.makedirs(path)

def get_text(url):####获取歌手主页信息
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Accept':'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
             'Cookie':'__utmc=94650624; WM_TID=Tw6wofkSY39ABVFUFUZ9aDNGfhlaL0qv; __utmz=94650624.1544246361.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; WM_NI=NS5nO%2FQ8mTkv31mO83h2%2BnPc%2B0FHR%2Bic6peIcuEqlvVFfRdUveV7OwHGK44fXKhtFnejUMuctTGV9e9ZH99w%2F1Gv7T%2F6HQnL2X%2F2tuSUv8Q29dCFyp7wpDz6v%2FXCQT0bZTY%3D; JSESSIONID-WYYY=y8ltGn5bWoyqlBt3h83fgcFagvceehsv%2B1ye1WWv1VT3jaboYcjqzlQd8xgJ%2BYQDwnFeIDqXyqEbpFnpgJKP9DJT8c9F9daxktY9rhObE5OjMFXGqcm2W1WEsyOy%5CfOYu5QWvnCpwSOYjXH59YBkKpM4i4%5CF0S7iZUh3GtyqllcqUymH%3A1544249900648; WM_NIKE=9ca17ae2e6ffcda170e2e6ee83ce6fb19aaf8ec56d83b88ba3c14b838b8e85b741fb98b9aac547e9ecaabbf92af0fea7c3b92a8e8dfb8fce2593e8a3b5ea7ef1efa3b0bb39aceee58fd369e9f08aa9d121abbdfa91e843a1ab8b92ef7e969aaab3e75fb6bb9ad8ce7d8c9985d5b76e9c95a895c566a7b69baef869b88c89b7bc6ffb8688dabc7dedef8997b660edea88b2ed48f288e1d3f77f918bbad9d43afbbc8da7fc7cf5a9c0a5f93eb6f198a4d460f4be96b5dc37e2a3; __utma=94650624.1228060768.1538964730.1538964730.1544246361.2; __utmb=94650624.27.10.1544246361; _iuqxldmzr_=32; __utmz=187553192.1539153528.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=187553192.1023355391.1538218652.1538218652.1539153528.2; __oc_uuid=7755f5e0-c3d6-11e8-a459-992c3c34cb4a; usertrack=ezq0o1ve4ASYlStxU31WAg==; _ntes_nnid=037acd55062793aa684c374f34f2124f,1538218652284; _ntes_nuid=037acd55062793aa684c374f34f2124f'}
    r=requests.get(url,headers=headers,timeout=20)
    soup=BeautifulSoup(r.text)
    return soup
####outpath=D:/lyrics/lyrics_singer/
def lyrics_singer(outpath):
    for k,v in singer_info.items():
        full_path=outpath+k+"/"
        try:#歌手名字含有非法字符
            mkdir(full_path)#####创建歌手文件夹
        except:
            continue
        url= 'https://music.163.com/artist?id='+v
        try:#读不到网页
            soup=get_text(url)
        except:
            continue
        for i in soup.find("ul",class_="f-hide").children:
            song_name=i.string#####获取i最里层的
            try:#####伴奏没歌词
                song_id=i.contents[0]['href'].replace('/song?id=','')####对i的子节点操作
            except:
                continue
            url_lyric='http://music.163.com/api/song/lyric?id='+song_id+'&lv=1&kv=1&tv=-1'
            try:####读不到网页
                lyric_html=requests.get(url_lyric)
            except:
                continue
            try:#网址内容格式异常
                mass_lyric=json.loads(lyric_html.text)
            except:
                continue
            try:####异常处理没歌词的歌
                init_lyric=mass_lyric['lrc']['lyric']
                pat = re.compile(r'\[.*\]')
                lyric=re.sub(pat, "", init_lyric)
            except:
                continue
            try:#### must be str, not NoneType
                full_name=full_path+song_name+'.txt'
            except:
                continue
            try:#####可能由文件名不合法，文件夹不存在有的歌名带/等等导致
                with open(full_name,'w',encoding='utf-8') as fp:
                    fp.write(lyric)
            except:
                pass

if __name__ == "__main__":
    outpath='D:/Lyrics/chinese/'
    lyrics_singer(outpath)