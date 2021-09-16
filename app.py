from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://3.34.252.62', 27017, username = "test", password = "test")

db = client.music_list




## index
@app.route('/')  # 메인페이지로 이동
def main():
    main_title = "H!"  # 진자 탬플릿언어에 사용될 내용
    subtitle = "들으면 기분좋아지는 여름노래 모음"
    music_list = list(db.music_list.find({}, {'_id': False}))
    return render_template("index.html", title=main_title, subtitle=subtitle, list=music_list)

# 상세페이지로 이동
@app.route('/detail/<title>')
def detail(title):
    ## db에서 title : title인 페이지 찾는다.
    music = db.music_list.find_one({'title':title},{'_id':False})
    ## 댓글 포함
    return render_template("detail.html", music = music )
# 로그인페이지로 이동
@app.route('/login')
def login():
    return render_template("login.html")

## like 버튼클릭시 호출
@app.route('/api/up', methods=['POST'])
def like():
    id_receive = request.args.get('id_give')
    target_like = db.music_list.find_one({'id': id_receive})
    current_like = target_like['like']

    new_like = current_like +1
    db.users.update_one({'id': id_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})





# @app.route('/test', methods=['GET'])
# def test_get():
#    title_receive = request.args.get('title_give')
#    print(title_receive)
#    return jsonify({'result':'success', 'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
