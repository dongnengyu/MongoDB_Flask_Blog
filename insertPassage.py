#!/usr/bin/python3
from datetime import datetime
import pymongo

"""
字段名	字段含义
title	文章的标题
content	文章的内容
category	文章的分类
author	文章的作者
slug	文章的url(如果是中文的话，给其起一个英文的名称，说是有利于搜索引擎的优化，有点不大明白)
published	文章是否发布
meta	搜集这个文章被赞了多少次，被踩了多少次。
comments	文章的评论
created	文章的创建时间
"""


def insertPassage(title, content, author):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['tutorial']
    mycol = mydb["movie"]
    mydict = {
        "title": title,
        "content": content,
        "author": author
    }

    # mydict = {
    #     "title": title,
    #     "directed_by": directed_by,
    #     "stars": [
    #         "Morgan Freeman",
    #         "Brad Pitt",
    #         "Kevin Spacey"
    #     ],
    #     "tags": [
    #         "drama",
    #         "mystery",
    #         "thiller"
    #     ],
    #     "debut": datetime(1995, 10, 21),
    #     "likes": 134370,
    #     "dislikes": 1037,
    #     "comments": [
    #         {
    #             "user": "user3",
    #             "message": "Love Kevin Spacey",
    #             "dateCreated": datetime(2002, 10, 12),
    #             "like": 0
    #         },
    #         {
    #             "user": "user2",
    #             "message": "Good works!",
    #             "dateCreated": datetime(2013, 11, 20),
    #             "like": 14
    #         },
    #         {
    #             "user": "user7",
    #             "message": "Good Movie!",
    #             "dateCreated": datetime(2009, 11, 10),
    #             "like": 2
    #         }
    #     ]
    # }

    x = mycol.insert_one(mydict)

    print(x.inserted_id)


insertPassage("潘康甜是傻逼", "我是说真的", "董能宇")
