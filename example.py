import requests
from bs4 import BeautifulSoup

url = 'https://www.melon.com/new/index.htm'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url,headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#frm > div > table > tbody > tr')

for tr in trs:
    img = tr.select_one('td:nth-child(3) > div > a > img')['src']
    title = tr.select_one('td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a').text
    artist = tr.select_one('td:nth-child(5) > div > div > div.ellipsis.rank02 > a').text
    print(img,title,artist)
# 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis