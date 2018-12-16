import csv

from pymongo import MongoClient
from gridfs import *

client = MongoClient('127.0.0.1', 27017)  # 连接mongodb
db = client.photo  # 连接对应数据库
# db.authenticate("username","passowd")
fs = GridFS(db, collection="images")  # 连接collection
print(fs.list())
print(fs.list().sort("filename"))
num = 1
for grid_out in fs.find(no_cursor_timeout=True):
    data = grid_out.read()  # 获取图片数据
    outf = open('/home/%d.jpg' % num, 'wb')
    outf.write(data)  # 存储图片
    outf.close()
    if num % 100000 == 0:
        metadata_file = open("/home/metadata%d.csv" % (num / 100000 + 1), "ab")
        csv_writer = csv.writer(metadata_file, delimiter='\t')
    row = [grid_out.photo_title.encode('utf-8'), grid_out.uploadDate, grid_out.upload_date, \
           grid_out.longitude, grid_out.latitude, grid_out.width, grid_out.height, \
           grid_out.owner_name.encode('utf-8'), grid_out.photo_id, grid_out._id, grid_out.photo_url]
    csv_writer.writerow(row)
