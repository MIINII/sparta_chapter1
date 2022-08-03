from flask import Flask, render_template, jsonify

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient(
    "mongodb+srv://chapter01:chapter01@chapter01.lnhgc.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=ca, )
db = client.chapter01


@app.route('/')
def main():
    return render_template("index.html")

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



# 카페 상세페이지 정보
@app.route('/cafe', methods=["GET"])
def cafe():
    cafe_list = list(db.cafes.find({}, {'_id': False}))
    cafe1 = cafe_list[0]
    return render_template('detail.html', cafe1=cafe1)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
