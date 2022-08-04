import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from pymongo import MongoClient
import random

client = MongoClient("mongodb+srv://chapter01:chapter01@chapter01.lnhgc.mongodb.net/?retryWrites=true&w=majority")
db = client.chapter01

driver = webdriver.Chrome('./chromedriver')  # 드라이버를 실행합니다.

url = "https://www.mangoplate.com/search/%EA%B2%BD%EC%A3%BC%20%EC%B9%B4%ED%8E%98?keyword=%EA%B2%BD%EC%A3%BC%20%EC%B9%B4%ED%8E%98&page=1"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url, headers=headers)

driver.get(url)  # 드라이버에 해당 url의 웹페이지를 띄웁니다.
sleep(5)  # 페이지가 로딩되는 동안 5초 간 기다립니다.

req = driver.page_source  # html 정보를 가져옵니다.
driver.quit()  # 정보를 가져왔으므로 드라이버는 꺼줍니다.

# soup = BeautifulSoup(data.text, 'html.parser')
soup = BeautifulSoup(req, 'html.parser')  # 가져온 정보를 beautifulsoup으로 파싱해줍니다.

cafes = soup.select("li.server_render_search_result_item > div.list-restaurant-item > .restaurant-item")

for cafe in cafes:
    name = cafe.select_one("figcaption > div.info > a > h2")
    span = name.select_one("span")
    if span is not None:
        name.select_one("span").decompose()
    names = name.text.strip()

    points = cafe.select_one("figcaption > div.info > strong").text
    if points == "":
        points = 3.0

    temp_hashtag = ['베이커리', '빙수', '커피', '디저트', '감성']
    temp_set = set()
    while True:
        if len(temp_set) == 3:
            break
        temp_set.add(temp_hashtag[random.randrange(0, 4)])

    info = cafe.select_one("a > div.thumb > img")
    location = info["alt"]
    location = location[len(names) + 6:]
    image = info["data-original"]

    headers = {
        "X-NCP-APIGW-API-KEY-ID": "cdwrnjl4um",
        "X-NCP-APIGW-API-KEY": "EKPvhqAvcefxiSSzY2rwobCnJMcxfFYBA1P6haxy"
    }
    r = requests.get(f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={location}", headers=headers)
    response = r.json()
    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])
            doc = {
                "title": names,
                "address": location,
                "image": image,
                "stars": points,
                "mapx": x,
                "mapy": y,
                "like_users": [],
                "hashtags": list(temp_set),
            }
            db.cafes.insert_one(doc)
