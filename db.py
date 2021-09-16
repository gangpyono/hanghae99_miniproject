import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('mongodb://3.34.252.62', 27017, username = "test", password = "test")

db = client.music_list

# 멜론사이트 이미지,제목,가수,앨범명 크롤링
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.melon.com/chart/month/index.htm?classCd=GN0000&moved=Y&rankMonth=202008',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
trs = soup.select('#frm > div > table > tbody >tr ')

count = 0
for tr in trs:
    if count > 20:
        break
    img = tr.select_one('td:nth-child(4) > div > a > img')['src']
    title = tr.select_one('td:nth-child(6) > div > div > div.ellipsis.rank01 > span > a').text.strip()
    artist = tr.select_one('td:nth-child(6) > div > div > div.ellipsis.rank02 > a').text.strip()
    album = tr.select_one('td:nth-child(7) > div > div > div > a').text.strip()
    url = ''
    doc = {'img': img, 'title': title, 'artist': artist, 'album' : album,'url': '' }
    db.music_list.insert_one(doc)
    count += 1


from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

