# -*- coding:utf-8
from bs4 import BeautifulSoup
import lxml
import requests
import re
import json

#####获取歌手id
def get_singerid(url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Accept':'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
             'Cookie':'__utmc=94650624; WM_TID=Tw6wofkSY39ABVFUFUZ9aDNGfhlaL0qv; __utmz=94650624.1544246361.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; WM_NI=NS5nO%2FQ8mTkv31mO83h2%2BnPc%2B0FHR%2Bic6peIcuEqlvVFfRdUveV7OwHGK44fXKhtFnejUMuctTGV9e9ZH99w%2F1Gv7T%2F6HQnL2X%2F2tuSUv8Q29dCFyp7wpDz6v%2FXCQT0bZTY%3D; JSESSIONID-WYYY=y8ltGn5bWoyqlBt3h83fgcFagvceehsv%2B1ye1WWv1VT3jaboYcjqzlQd8xgJ%2BYQDwnFeIDqXyqEbpFnpgJKP9DJT8c9F9daxktY9rhObE5OjMFXGqcm2W1WEsyOy%5CfOYu5QWvnCpwSOYjXH59YBkKpM4i4%5CF0S7iZUh3GtyqllcqUymH%3A1544249900648; WM_NIKE=9ca17ae2e6ffcda170e2e6ee83ce6fb19aaf8ec56d83b88ba3c14b838b8e85b741fb98b9aac547e9ecaabbf92af0fea7c3b92a8e8dfb8fce2593e8a3b5ea7ef1efa3b0bb39aceee58fd369e9f08aa9d121abbdfa91e843a1ab8b92ef7e969aaab3e75fb6bb9ad8ce7d8c9985d5b76e9c95a895c566a7b69baef869b88c89b7bc6ffb8688dabc7dedef8997b660edea88b2ed48f288e1d3f77f918bbad9d43afbbc8da7fc7cf5a9c0a5f93eb6f198a4d460f4be96b5dc37e2a3; __utma=94650624.1228060768.1538964730.1538964730.1544246361.2; __utmb=94650624.27.10.1544246361; _iuqxldmzr_=32; __utmz=187553192.1539153528.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=187553192.1023355391.1538218652.1538218652.1539153528.2; __oc_uuid=7755f5e0-c3d6-11e8-a459-992c3c34cb4a; usertrack=ezq0o1ve4ASYlStxU31WAg==; _ntes_nnid=037acd55062793aa684c374f34f2124f,1538218652284; _ntes_nuid=037acd55062793aa684c374f34f2124f'}
    r = requests.get(url, headers=headers)
    soup=BeautifulSoup(r.text)
    #print(soup.prettify())
    for artist in soup.find_all('a',class_="nm nm-icn f-thide s-fc0"):
        singer_name=artist.text###歌手名
        #print(singer_name)
        #print(str(artist))
        singer_id=artist['href'].replace('/artist?id=', '').strip()
        #print(singer_id)
        singer[singer_name]=singer.get(singer_name,singer_id)



if __name__ == "__main__":
    singer={}####["林俊杰"：3648，...]，歌手和对应的id
    huayu_id_list=[1001,1002,1003]#####三类华语歌手页面网址的id
    category_id_list=[65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,0]#######每类华语歌手下细分类的id
    for i in huayu_id_list:
        for j in category_id_list:
            url='http://music.163.com/discover/artist/cat?id='+str(i)+'&initial='+str(j)
            get_singerid(url)
    print(len(singer))####看下长度
    with open(r'/Users/cathy/Documents/python_script/music/data/singer_id.txt','w',encoding="UTF-8") as fp:
        json.dump(singer,fp)






