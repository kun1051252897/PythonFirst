import codecs
import datetime
import time
import urllib.request
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250'


# 下载图片
def getImg(url, name):
    response = urllib.request.urlopen("url")
    cat_img = response.read()
    with open(name+'.webp', 'wb') as f:
        f.write(cat_img)


def parseHtml(html):
    # 解析html 从每个节点获取对应信息
    soup = BeautifulSoup(html, 'html.parser')
    movie_list_grid = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []
    for movie_li in movie_list_grid.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})
        detail_pic = movie_li.find('div', attrs={'class': 'pic'})
        detail_pic_url = detail_pic.find('img').getScr()
        getImg(detail_pic_url, datetime.datetime.now())
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        movie_name_list.append(movie_name)
        print(movie_name)

    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None


# 获取豆瓣排行榜
def getMovieTop():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.80 Safari/537.36 '
    }
    url = DOWNLOAD_URL
    # 创建本地文件
    with codecs.open('movies', 'wb', encoding='utf-8') as fp:
        while url:
            # 读取url内容
            # request = requests.Session()
            # request.proxies = {"http": "http://10.10.1.10:3128", }
            response = requests.get(url, headers=headers).content
            # 解析html
            movies, url = parseHtml(response)
            # 写入文件中
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))


def getMovie():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.80 Safari/537.36 '
    }
    response = requests.get("https://www.jht3hddmxlqo.com/index/home.html", headers=headers).content
    print(response.decode('utf-8'))


if __name__ == '__main__':
    getMovieTop()
