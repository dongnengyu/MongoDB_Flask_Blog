# coding:utf-8

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pymongoUtils import GFS
import sys

app = Flask(__name__)


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
        query = {'filename': filename}
        id = gfs.insertFile(file_db, filePath, query)  # 插入文件
        id = gfs.getID(file_db, query)
        print(id)
        print(gfs.listFile(file_db))
        ################

        ##将文件插入数据库之后就删除本地硬盘的文件

        return redirect(url_for('uploadSuccess'))

    else:
        return render_template('upload.html')


@app.route('/uploadSuccess', methods=['POST', 'GET'])
def uploadSuccess():
    return render_template('uploadSuccess.html')


@app.route('/downloads', methods=['POST', 'GET'])
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

            ##打印输出文件路径
            print (sys.argv[0])
        else:
            print("数据库中不存在该文件，请上传")
    return render_template('downloads.html')


if __name__ == '__main__':
    app.run(debug=True)
