from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient("mongodb+srv://chapter01:chapter01@chapter01.lnhgc.mongodb.net/?retryWrites=true&w=majority",
                     tlsCAFile=ca)
db = client.chapter01

doc = {
  'title': '00카페',
  'phone': '010-0000-02200'
}

db.title.insert_one(doc)
