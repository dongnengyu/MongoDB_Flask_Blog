# coding:utf-8
import datetime
import mimetypes

import pymongo
from pymongo import MongoClient
import flask
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pymongoUtils import GFS
from flask import jsonify

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def inde():
    return redirect('/index')


@app.route('/index', methods=['POST', 'GET'])
def index():
    ######从数据库中读取5条数据显示在首页
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient['fileDB']

    a = db.posts.find().sort([("date", -1)])

    post1 = a[0]['title']
    post2 = a[1]['title']
    post3 = a[2]['title']
    post4 = a[3]['title']
    post5 = a[4]['title']

    print(post1)

    return jsonify({'ok': True})

    return render_template(
        'index.html',
        post1=post1,
        post2=post2,
        post3=post3,
        post4=post4,
        post5=post5,

        link1="post/" + post1,
        link2="post/" + post2,
        link3="post/" + post3,
        link4="post/" + post4,
        link5="post/" + post5,

    )


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/uploads',
                                   secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        print(f.filename)
        print(f)
        print(basepath)
        print(upload_path)

        # 将文件插入数据库
        gfs = GFS('fileDB', 'fileTable')
        (file_db, fileTable) = gfs.createDB()  # 创建数据库与数据表
        filePath = upload_path  # 插入的文件
        filename = (filePath.split('/')[-1])  # 获取插入文件的文件名
        mime = mimetypes.guess_type(filename)[0]  # 获取上传文件的MIME类型
        query = {'filename': filename, 'mime': mime}
        id = gfs.insertFile(file_db, filePath, query)  # 插入文件
        if id == None:
            id = gfs.getID(file_db, query)
        print(id)
        print(gfs.listFile(file_db))
        print("上传成功")
        ################

        ##将文件插入数据库之后就删除本地硬盘的文件
        os.remove(upload_path)
        print("插入数据库成功，删除上传文件")

        fid = id
        return flask.redirect('/upload/' + str(fid))

    else:
        return render_template('upload.html')


@app.route('/upload/<fid>', methods=['POST', 'GET'])
def uploadSuccess(fid):
    try:
        gfs = GFS('fileDB', 'fileTable')
        (file_db, fileTable) = gfs.createDB()  # 创建数据库与数据表
        (bdata, attri) = gfs.getFile(file_db, ObjectId(fid))  # 查询并获取文件信息至内存

        print(attri)

        print(attri.get('mime'))

        return flask.Response(bdata, mimetype=attri.get('mime'))
    except IOError:
        print("dd")

        # return render_template('uploadSuccess.html')


@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == 'POST':
        filename = request.form['filename']
        print(filename)
        gfs = GFS('fileDB', 'fileTable')
        (file_db, fileTable) = gfs.createDB()  # 创建数据库与数据表

        # 打印出数据库中的文件
        print(gfs.listFile(file_db))

        if filename in gfs.listFile(file_db):
            print("数据库中存在该文件，将会被读取到硬盘")
            query = {'filename': filename}
            id = gfs.getID(file_db, query)
            print(id)
            (bdata, attri) = gfs.getFile(file_db, id)  # 查询并获取文件信息至内存
            gfs.write_2_disk(bdata, attri)  # 写入磁盘

        else:
            print("数据库中不存在该文件，请上传")
    return render_template('download.html')


@app.route("/download/<filepath>", methods=['GET'])
def download_file(filepath):
    # 此处的filepath是文件的路径，但是文件必须存储在static文件夹下， 比如images\test.jpg
    return app.send_static_file(filepath)


@app.route("/post/<postname>", methods=['GET'])
def download_file1(postname):
    print(postname)

    Client = MongoClient()
    db = Client.fileDB

    posts = db.posts

    post = {'title': postname}

    print(post)

    content = posts.find(post)[0]

    time = content['date']
    print(time.year)

    print(content)
    print(content['title'])

    return render_template(
        'post.html',
        title=content['title'],
        author="董能宇",
        main_content=content['content'],
        post_time=str(time.year) + "-" + str(time.month) + "-" + str(time.day)
    )


@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin/login.html')


@app.route("/admin/index", methods=['GET'])
def admin1():
    return render_template('admin/index.html')


@app.route("/HIbernate和Mybatis优缺点对比", methods=["GET"])
def admin11():
    filename = "IMG_0087.PNG"
    print(filename)
    gfs = GFS('fileDB', 'fileTable')
    (file_db, fileTable) = gfs.createDB()  # 创建数据库与数据表

    # 打印出数据库中的文件
    print(gfs.listFile(file_db))

    if filename in gfs.listFile(file_db):
        print("数据库中存在该文件，将会被读取到硬盘")
        query = {'filename': filename}
        id = gfs.getID(file_db, query)
        print(id)
        (bdata, attri) = gfs.getFile(file_db, id)  # 查询并获取文件信息至内存
        gfs.write_2_disk(bdata, attri)  # 写入磁盘

        return render_template(
            'HIbernate和Mybatis优缺点对比.html',
            title="download/" + filename
        )
    else:
        return render_template(
            'HIbernate和Mybatis优缺点对比.html',
            title="download/" + filename
        )


@app.route("/write", methods=['GET', 'POST'])
def write():
    # if request.method == 'POST':
    #     content = request.form['content']
    #     print(content)
    #
    #     title = request.form['title']
    #
    #     now = datetime.datetime.now()
    #
    #     print(now)
    #
    #     Client = MongoClient()
    #     db = Client.fileDB
    #
    #     post = {'content': content, 'title': title, 'date': now}
    #
    #     posts = db.posts
    #
    #     post_1 = posts.insert_one(post).inserted_id
    #
    #     print(post_1)

    return render_template("write.html")


@app.route("/write/save", methods=['GET', 'POST'])
def savePassage():
    if request.method == 'POST':
        content1 = request.get_json()
        print(content1)

        print(content1['content'])

        content = content1['content']

        title = content1['title']

        print(title)

        now = datetime.datetime.now()

        print(now)

        Client = MongoClient()
        db = Client.fileDB

        post = {'content': content, 'title': title, 'date': now}

        posts = db.posts

        post_1 = posts.insert_one(post).inserted_id

        print(post_1)

        return jsonify({'ok': True})

    return render_template("write.html")


@app.route("/test", methods=["GET", "POST"])
def test():
    print("dd")
    print(request.get_data())
    data = request.get_json()
    print(data)

    return jsonify({'ok': True})
    return render_template("test.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8090, debug=True)
