from pymongo import MongoClient
from gridfs import *
import requests

dic = {
    "photo_url": "http://api.mongodb.com/python/current/api/gridfs/errors.html",
    "filename": "http://api.mongodb.com/python/current/api/gridfs/errors.html"
}

client = MongoClient('127.0.0.1', 27017)  # 连接mongodb
db = client.photo  # 连接对应数据库
# db.authenticate("username","passowd")
fs = GridFS(db, collection="images")  # 连接collection
data = requests.get(dic["photo_url"], timeout=10).content
print(data)
# 确认数据库中不存在此图片之后再保存
if not fs.find_one({"photo_url": dic["photo_url"], "filename": dic["filename"]}):
    fs.put(data, **dic)
# 上传成功后，photo数据库下出现两个collection，分别为: images.files, images.chunks
