from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi

ca = certifi.where()

## mongodb
client = MongoClient(
    "mongodb+srv://chapter01:chapter01@chapter01.lnhgc.mongodb.net/?retryWrites=true&w=majority",
)
db = client.chapter01
####################

app = Flask(__name__)

@app.route('/main', methods=['GET'])
def cafe_list():
    cafe_list = list(db.cafes.find({}))
    return render_template("cafes.html", cafe_list=cafe_list)

# 카페 정보 detail로 들어가기
@app.route('/<detail>', methods=["GET"])
def cafe_detail(detail):
    cafe = db.cafes.find_one({'title':detail})
    return render_template("detail.html",cafe=cafe)

# 좋아요 누르기
@app.route('/like', methods=['POST'])
def like():
    username_receive = request.form["username_give"]
    post_title_recieve = request.form['post_title_give']

    db.cafes.update_one({'title':str(post_title_recieve)}, {'$addToSet' : {"like_user" : username_receive}})

    return jsonify({'msg':'좋아요'})



@app.route('/map')
def cafe_map():
    return render_template("map.html")


# 지도용 맛집리스트
@app.route('/matjip', methods=["GET"])
def get_matjip():
    # 맛집 목록을 반환하는 API
    matjip_list = list(db.cafes.find({}, {'_id': False}))
    # matjip_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success', 'matjip_list': matjip_list})




@app.route("/comment", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']

    comment_list = list(db.comment.find({}, {'_id': False}))
    count = len(comment_list) + 1

    doc = {
        'num':count,
        'comment':comment_receive,
        'done':0
    }

    db.comment.insert_one(doc)

    return jsonify({'msg': '등록을 완료하였습니다.'})


@app.route("/comment_delete", methods=["POST"])
def comment_delete():
    num_receive = request.form['num_give']
    db.comment.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제를 완료하였습니다.'})


@app.route("/comment", methods=["GET"])
def comment_get():
    comment_list = list(db.comment.find({}, {'_id': False}))
    return jsonify({'comments': comment_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)