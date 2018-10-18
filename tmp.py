# -*- coding: utf-8 -*-
'''
import pandas as pd
import pymysql.cursors
import pymysql
import pandas as pd
import numpy as np
from texttable import Texttable

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
df_movie = df_movie.filter(items=[ 'id','title','type'], axis=1)

df_user=df_user.drop('rates',axis=1).join(df_user['rates'].str.split(",",expand=True).stack().reset_index(level=1,drop=True).rename('rates'))
df_user['user_movie_id']=df_user['rates'].str.split("'").str[1]
df_user['movie_score']=df_user['rates'].str.split("'").str[3]
df_user=df_user.drop('rates',axis=1)

ratings=np.array(df_user).tolist()
# -*- coding: utf-8 -*-

name_movie_rate_Dict = {}
movie_name = {}

n=10
def formatuserDict(userId, l):#输入user和邻居的电影评分列表，返回user和邻居对各电影的评分
    user = {}
    for i in name_movie_rate_Dict[userId]:
        user[i[0]] = [i[1], 0]
    for j in name_movie_rate_Dict[l]:
        if(j[0] not in user):
            user[j[0]] = [0, j[1]]
        else:
            user[j[0]][1] = j[1]
    return user

def getCost(userId, l):
    user =formatuserDict(userId, l)# 获取用户userId和l评分电影的并集 # {'电影ID'：[userId的评分，l的评分]} 没有评分为0
    x = 0.0
    y = 0.0
    z = 0.0
    for k, v in user.items():
        x += float(v[0]) * float(v[0])
        y += float(v[1]) * float(v[1])
        z += float(v[0]) * float(v[1])
    if (z == 0.0):
        return 0
    return z / ((x * y)**0.5)


for i in ratings:
    tmp=(i[1],float(i[2])/5)
    if(i[0] in name_movie_rate_Dict):
        name_movie_rate_Dict[i[0]].append(tmp)
    else:
        name_movie_rate_Dict[i[0]]=[tmp]
    if(i[1] in movie_name):
        movie_name[i[1]].append(i[0])
    else:
        movie_name[i[1]]=[i[0]]


neighbors = []
neighbors2=[]
for i in name_movie_rate_Dict["88180115"]:
    for j in movie_name[i[0]]:
        if (j!= "88180115" and j not in neighbors):
            neighbors.append(j)  # 计算这些用户与userId的相似度并排序
#print(neighbors)
for i in neighbors:
    dist = getCost('88180115',i)#返回user和各邻居的相似度评分列表
    neighbors2.append([dist, i]) #返回评分和邻居对应列表
    neighbors2.sort(reverse=True)# 排序默认是升序，reverse=True表示降序
    neighbors2 = neighbors2[:10]

#print(neighbors2)

recommandList = []
# 建立推荐字典
recommandDict = {}#前十个邻居推荐电影的相似度加分
for neighbor in neighbors2:#评分和邻居对的列表
    movies = name_movie_rate_Dict[neighbor[1]]#第一个对的邻居看的电影列表
    for movie in movies:
        if (movie[0] in recommandDict):
            recommandDict[movie[0]] += neighbor[0]#该电影加上相似度分
        else:
            recommandDict[movie[0]] = neighbor[0]
# 建立推荐列表
for key in recommandDict:
    recommandList.append([recommandDict[key], key])#更改为列表，列表可以排序,[相似度总和评分,电影]
recommandList.sort(reverse=True)
recommandList = recommandList[:n]#排出前十个推荐的电影，[相似度总和评分,电影]
print("recommandList=",recommandList)


user = [i[0] for i in name_movie_rate_Dict["88180115"]]#user看过的电影
recommand = [i[1] for i in recommandList]
count = 0.0
if (len(user) >= len(recommand)):
    for i in recommand:
        if (i in user):
            count += 1.0
    cost = count / len(recommand)
else:
    for i in user:
        if (i in recommand):
            count += 1.0
    cost = count / len(user)

print("cost=",cost)

movies=np.array(df_movie).tolist()
print(type(movies),movies[0])

neighbors_id = [i[1] for i in neighbors2]#根据相似度排名的邻居
table = Texttable()
table.set_deco(Texttable.HEADER)
table.set_cols_dtype(["t", "t", "t"])
table.set_cols_align(["l", "l", "l"])
rows = []
movie2=[]
rows.append(["movie ID","Name","release"])
for item in recommandList:#[相似度总和,电影id# ]
    for i in movies:
        if i[0] == item[1]:
            movie2 = i#[电影id，电影名,电影类型]
            break
    rows.append(movie2)
print(rows)
table.add_rows(rows)
print(table.draw())
'''
from texttable import Texttable
table = Texttable()
table.set_deco(Texttable.HEADER)
table.set_cols_dtype(["t", "t", "t", "t"])
table.set_cols_align(["l", "l", "l", "l"])
table.add_rows([["a","b","c","d"],["aa","bb","cc","dd"]])
print(table.draw())





