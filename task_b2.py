# -*- coding: utf-8 -*-
import pandas as pd
import pymysql.cursors
import pymysql
import pandas as pd
import numpy as np
config = {
    'host': '127.0.0.1',
    'port': 3306,  # MySQL默认端口
    'user': 'root',  # mysql默认用户名
    'password': 'tangao65267237',
    'db': 'douban',  # 数据库
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
# 创建连接
con = pymysql.connect(**config)  # 字典形式

# 执行sql语句
try:
    with con.cursor() as cursor:
        sql = "select * from user"
        cursor.execute(sql)
        result = cursor.fetchall()
finally:
    con.close();
df_user = pd.DataFrame(result)

# 创建连接
con = pymysql.connect(**config)

# 执行sql语句
try:
    with con.cursor() as cursor:
        sql = "select * from movie"
        cursor.execute(sql)
        result = cursor.fetchall()
finally:
    con.close();
df_movie = pd.DataFrame(result)

df_user = df_user.filter(items=['name', 'rates'], axis=1)
df_movie = df_movie.filter(items=['title', 'id'],axis=1)

df_user=df_user.drop('rates',axis=1).join(df_user['rates'].str.split(",",expand=True).stack().reset_index(level=1,drop=True).rename('rates'))
df_user['user_movie_id']=df_user['rates'].str.split("'").str[1]
df_user['movie_score']=df_user['rates'].str.split("'").str[3]
df_user=df_user.drop('rates',axis=1)

ratings=np.array(df_user).tolist()
movies=np.array(df_movie).tolist()

from numpy import *
import time
from texttable import Texttable
class CF:
    def __init__(self, movies, ratings, k=5, n=10):
        self.movies = movies
        self.ratings = ratings
        self.k = k #邻居个数
        self.n = n #推荐个数
        self.name_movie_rate_Dict = {} #用户对电影评分，{'UserID：用户ID':[(MovieID：电影ID,Rating：用户对电影的评星)]}
        self.movie_name = {} #对某电影评分的用户，数据格式：{'MovieID：电影ID',[UserID：用户ID]}
        self.neighbors = [] #邻居列表
        self.recommandList = [] #推荐列表
        self.score = 0.0 #推荐准确率评分

    #基于用户，根据对电影的评分计算用户之间的相似度
    def recommendByName(self, userId):
        self.format_user_table()
        self.n = len(self.name_movie_rate_Dict[userId])
        self.getNearestNeighbor(userId)
        self.getrecommandList(userId)
        self.getPrecision(userId)

    def format_user_table(self):
        for i in ratings:
            tmp = (i[1], float(i[2]) / 5)
            if (i[0] in self.name_movie_rate_Dict):
                self.name_movie_rate_Dict[i[0]].append(tmp)
            else:
                self.name_movie_rate_Dict[i[0]] = [tmp]
            if (i[1] in self.movie_name):
                self.movie_name[i[1]].append(i[0])
            else:
                self.movie_name[i[1]] = [i[0]]

    def getNearestNeighbor(self, userId):
        neighbors = []
        self.neighbors = []
        for i in self.name_movie_rate_Dict[userId]:
            for j in self.movie_name[i[0]]:
                if (j != userId and j not in neighbors):
                    neighbors.append(j)  # 计算这些用户与userId的相似度并排序
        for i in neighbors:
            dist = self.getCost(userId,i)
            self.neighbors.append([dist, i]) # 排序默认是升序，reverse=True表示降序
            self.neighbors.sort(reverse=True)
            self.neighbors = self.neighbors[:self.k]

    def formatuserDict(self, userId, l):  # 输入user和邻居的电影评分列表，返回user和邻居对各电影的评分
        user = {}
        for i in self.name_movie_rate_Dict[userId]:
            user[i[0]] = [i[1], 0]
        for j in self.name_movie_rate_Dict[l]:
            if (j[0] not in user):
                user[j[0]] = [0, j[1]]
            else:
                user[j[0]][1] = j[1]
        return user

    def getCost(self, userId,l):  #获取用户userId和l评分电影的并集 # {'电影ID'：[userId的评分，l的评分]} 没有评分为0
        user = self.formatuserDict(userId, l)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0]) * float(v[0])
            y += float(v[1]) * float(v[1])
            z += float(v[0]) * float(v[1])
        if(z == 0.0):
            return 0
        return z / sqrt(x * y)

    def getrecommandList(self, userId):
        self.recommandList = []
        # 建立推荐字典
        recommandDict = {}
        for neighbor in self.neighbors:
            movies = self.name_movie_rate_Dict[neighbor[1]]
            for movie in movies:
                if(movie[0] in recommandDict):
                    recommandDict[movie[0]] += neighbor[0]
                else:
                    recommandDict[movie[0]] = neighbor[0]
        # 建立推荐列表
        for key in recommandDict:
            self.recommandList.append([recommandDict[key], key])
        self.recommandList.sort(reverse=True)
        self.recommandList = self.recommandList[:self.n]

    def getPrecision(self, userId):
        user = [i[0] for i in self.name_movie_rate_Dict[userId]]
        recommand = [i[1] for i in self.recommandList]
        count = 0.0
        if(len(user) >= len(recommand)):
            for i in recommand:
                if(i in user):
                    count += 1.0
                    self.cost = count / len(recommand)
                else:
                    for i in user:
                        if(i in recommand):
                            count += 1.0
                        self.cost = count / len(user)

    def showTable(self):
        neighbors_id = [i[1] for i in self.neighbors]

        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_dtype(["t", "t", "t", "t"])
        table.set_cols_align(["l", "l", "l", "l"])
        rows = []
        movie=[]
        rows.append([u"movie ID", u"Name", u"release", u"from userID"])
        for item in self.recommandList:
            fromID = []
            for i in self.movies:
                if i[0] == item[1]:
                    movie = i
                    break
            for i in self.movie_name[item[1]]:
                if i in neighbors_id:
                    fromID.append(i)
            movie.append(fromID)
            rows.append(movie)
        table.add_rows(rows)
        print(table.draw())

start = time.clock()
demo = CF(movies, ratings, k=20)
demo.recommendByName("88180115")
print("推荐列表为：")
demo.showTable()
print("处理的数据为%d条" % (len(demo.ratings)))
print("准确率： %.2f %%" % (demo.cost * 100))
end = time.clock()
print("耗费时间： %f s" % (end - start))

