# from multiprocessing.sharedctypes import Value
from pymongo import MongoClient
import jwt
import datetime
import hashlib
import certifi
from flask import Flask, render_template, jsonify, request, redirect, url_for
# from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

ca = certifi.where()
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["UPLOAD_FOLDER"] = "./static/profile_pics"

## mongodb
SECRET_KEY = "chapter01"

client = MongoClient(
  "mongodb+srv://chapter01:chapter01@chapter01.lnhgc.mongodb.net/?retryWrites=true&w=majority",
  tlsCAFile=ca,
)
db = client.chapter01
####################

app = Flask(__name__)


###################################################################


#################################
##  HTML을 주는 부분##        ##
#################################

# @app.route("/main", methods=['GET'])
# def home():
#   try:
#     token_receive = request.cookies.get("mytoken")
#     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
#     user_info = db.user.find_one({"id": payload["id"]})
#     cafe_list = list(db.cafes.find({}))
#     return render_template("cafes.html", user_info=user_info, cafe_list=cafe_list)
#   except jwt.ExpiredSignatureError:
#     return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
#   except jwt.exceptions.DecodeError:
#     return redirect(url_for("register", msg="로그인 정보가 존재하지 않습니다."))

@app.route("/", methods=['GET'])
def home():
  token_receive = request.cookies.get("mytoken")
  try:
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
    user_info = db.user.find_one({"id": payload["id"]})
    return render_template(url_for("main", user_info=user_info))
  except jwt.ExpiredSignatureError:
    return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
  except jwt.exceptions.DecodeError:
    return redirect(url_for("register", msg="로그인 정보가 존재하지 않습니다."))


@app.route("/login")
def login():
  msg = request.args.get("msg")
  return render_template("login.html", msg=msg)


@app.route("/register")
def register():
  return render_template("register.html")


#################################
##  로그인을 위한 API          ##
#################################

# [아이디 중복확인]
@app.route("/register/check_dup", methods=["POST"])
def check_dup():
  username_receive = request.form["username_give"]
  exists = bool(db.user.find_one({"id": username_receive}))
  return jsonify({"result": "success", "exists": exists})


# [회원가입 API]
@app.route("/register/save", methods=["POST"])
def api_register():
  id_receive = request.form["id_give"]
  pw_receive = request.form["pw_give"]
  nickname_receive = request.form["nickname_give"]
  
  pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()
  # pw2_hash = hashlib.sha256(pw2_receive.encode("utf-8")).hexdigest()
  
  doc = {"id": id_receive, "pw": pw_hash, "nick": nickname_receive}
  
  db.user.insert_one(doc)
  return jsonify({"result": "success"})


# [로그인]
@app.route("/login/sign_in", methods=["POST"])
def sign_in():
  # 로그인
  username_receive = request.form["username_give"]
  password_receive = request.form["password_give"]
  
  pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
  result = db.user.find_one({"id": username_receive, "pw": pw_hash})
  
  if result is not None:
    payload = {
      "id": username_receive,
      "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),  # 로그인 24시간 유지
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256").decode("utf-8")
    
    return jsonify({"result": "success", "token": token})
  # 찾지 못하면
  else:
    return jsonify({"result": "fail", "msg": "아이디/비밀번호가 일치하지 않습니다."})


#################################
##  main.html 부분인가봐요##   ##
#################################

# 카페 정보 detail로 들어가기
@app.route('/<detail>', methods=["GET"])
def cafe_detail(detail):
  cafe = db.cafes.find_one({'title': detail})
  return render_template("detail.html", cafe=cafe)


# 좋아요 누르기
@app.route('/like', methods=['POST'])
def like():
  username_receive = request.form["username_give"]
  post_title_recieve = request.form['post_title_give']
  
  db.cafes.update_one({'title': str(post_title_recieve)}, {'$addToSet': {"like_user": username_receive}})
  
  return jsonify({'msg': '좋아요'})


#################################
##  map.html 부분##            ##
#################################
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


#################################
##  detail.html 부분##         ##
#################################
@app.route('/map')
@app.route("/comment", methods=["POST"])
def comment_post():
  comment_receive = request.form['comment_give']
  
  comment_list = list(db.comment.find({}, {'_id': False}))
  count = len(comment_list) + 1
  
  doc = {
    'num': count,
    'comment': comment_receive,
    'done': 0
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
