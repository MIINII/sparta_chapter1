from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

client = MongoClient('mongodb+srv://chapter01:chapter01@chapter01.lnhgc.mongodb.net/?retryWrites=true&w=majority')
db = client.chapter01

app = Flask(__name__)


@app.route('/')
def main():
    cafe_list = list(db.cafes.find({}))
    return render_template("cafes.html", cafe_list=cafe_list)

@app.route('/like')
def like():
    like_state = request.form['like_give']
    return jsonify({'msg':'좋아요'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)