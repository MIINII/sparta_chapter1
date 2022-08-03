<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.cjl2gkt.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta
=======
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://chapter01:chapter01@chapter01.lnhgc.mongodb.net/?retryWrites=true&w=majority",
)
db = client.chapter01

app = Flask(__name__)

@app.route('/', methods=['GET'])
def cafe_list():
    cafe_list = list(db.cafes.find({}))
    return render_template("cafes.html", cafe_list=cafe_list)

@app.route('/<detail>')
def cafe_detail(detail):
    cafe = db.cafes.find_one({'title':detail})
    return render_template("detail.html", result=cafe)

@app.route('/like', methods=['POST'])
def like():
    username_receive = request.form["username_give"]
    post_title_recieve = request.form['post_title_give']

    db.cafes.update_one({'title':str(post_title_recieve)}, {'$addToSet' : {"like_user" : username_receive}})

    return jsonify({'msg':'좋아요'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
>>>>>>> da80a0728e67d95bb19076f21c0602051aa73aaf
