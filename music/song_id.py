import requests
import json
from bs4 import BeautifulSoup

with open('/Users/cathy/Documents/python_script/music/singer_id.json','r',encoding='utf-8') as fp:
    singer_info=json.load(fp)#####歌手信息

def get_text(url):####获取歌手主页信息
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Accept':'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
             'Cookie':'__utmc=94650624; WM_TID=Tw6wofkSY39ABVFUFUZ9aDNGfhlaL0qv; __utmz=94650624.1544246361.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; WM_NI=NS5nO%2FQ8mTkv31mO83h2%2BnPc%2B0FHR%2Bic6peIcuEqlvVFfRdUveV7OwHGK44fXKhtFnejUMuctTGV9e9ZH99w%2F1Gv7T%2F6HQnL2X%2F2tuSUv8Q29dCFyp7wpDz6v%2FXCQT0bZTY%3D; JSESSIONID-WYYY=y8ltGn5bWoyqlBt3h83fgcFagvceehsv%2B1ye1WWv1VT3jaboYcjqzlQd8xgJ%2BYQDwnFeIDqXyqEbpFnpgJKP9DJT8c9F9daxktY9rhObE5OjMFXGqcm2W1WEsyOy%5CfOYu5QWvnCpwSOYjXH59YBkKpM4i4%5CF0S7iZUh3GtyqllcqUymH%3A1544249900648; WM_NIKE=9ca17ae2e6ffcda170e2e6ee83ce6fb19aaf8ec56d83b88ba3c14b838b8e85b741fb98b9aac547e9ecaabbf92af0fea7c3b92a8e8dfb8fce2593e8a3b5ea7ef1efa3b0bb39aceee58fd369e9f08aa9d121abbdfa91e843a1ab8b92ef7e969aaab3e75fb6bb9ad8ce7d8c9985d5b76e9c95a895c566a7b69baef869b88c89b7bc6ffb8688dabc7dedef8997b660edea88b2ed48f288e1d3f77f918bbad9d43afbbc8da7fc7cf5a9c0a5f93eb6f198a4d460f4be96b5dc37e2a3; __utma=94650624.1228060768.1538964730.1538964730.1544246361.2; __utmb=94650624.27.10.1544246361; _iuqxldmzr_=32; __utmz=187553192.1539153528.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=187553192.1023355391.1538218652.1538218652.1539153528.2; __oc_uuid=7755f5e0-c3d6-11e8-a459-992c3c34cb4a; usertrack=ezq0o1ve4ASYlStxU31WAg==; _ntes_nnid=037acd55062793aa684c374f34f2124f,1538218652284; _ntes_nuid=037acd55062793aa684c374f34f2124f'}
    r=requests.get(url,headers=headers,timeout=20)
    soup=BeautifulSoup(r.text)
    return soup

####outpath=D:/lyrics/lyrics_singer/
def lyrics_singer():
    song_dict={}  # 歌曲id
    for k,v in singer_info.items():
        url= 'https://music.163.com/artist?id='+v
        try:  # 读不到网页
            soup=get_text(url)
        except:
            continue
        try:
            for i in soup.find("ul",class_="f-hide").children:
                try:  # 伴奏没歌词
                    song_name=i.string  # 获取i最里层的
                    song_id=i.contents[0]['href'].replace('/song?id=','')  # 对i的子节点操作
                    song_dict[song_name]=song_dict(song_name,song_id)
                except:
                    continue
        except:
            pass           
    with open('/Users/cathy/Documents/python_script/music/song_id.json','w',encoding='utf-8') as fp:
        json.dump(song_dict,fp)
           
if __name__ == "__main__":
    lyrics_singer()
    