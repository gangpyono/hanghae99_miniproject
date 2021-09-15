from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.music_list


## index
@app.route('/')  # 메인페이지로 이동
def main():
    main_title = "H!"  # 진자 탬플릿언어에 사용될 내용
    subtitle = "들으면 기분좋아지는 여름노래 모음"

    # 멜론사이트 이미지,가수,제목 크롤링
    url = 'https://www.melon.com/new/index.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('#frm > div > table > tbody > tr')
    for tr in trs:
        img = tr.select_one('td:nth-child(3) > div > a > img')['src']
        title = tr.select_one('td:nth-child(5) > div > div > div.ellipsis.rank01 > span > a').text
        artist = tr.select_one('td:nth-child(5) > div > div > div.ellipsis.rank02 > a').text

        doc = {'img': img, 'title': title, 'artist' : artist }
        db.music_list.insert_one(doc)

    music_list = list(db.music_list.find({}, {'_id': False}))


    return render_template("index.html", title=main_title, subtitle=subtitle, list=music_list)

# 상세페이지로 이동
@app.route('/detail/<title>')
def detail(title):

##
    ## db에서 title : title인 페이지 찾는다.
    music = db.music_list.find_one({'title':title},{'_id':False})
    ## 댓글 포함
    return render_template("detail.html", music = music )

# 로그인페이지로 이동
@app.route('/login')
def login():
    return render_template("login.html")

## like 버튼클릭시 호출
@app.route('/', methods=['POST'])
def like():
    like_receive = request.args.get('like_give')
    ## like 업데이트
    return jsonify({'result': 'success'})





# @app.route('/test', methods=['GET'])
# def test_get():
#    title_receive = request.args.get('title_give')
#    print(title_receive)
#    return jsonify({'result':'success', 'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
