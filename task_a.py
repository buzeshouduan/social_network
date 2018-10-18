#读取mysql数据
import pymysql.cursors
import pymysql
import pandas as pd

config = {
    'host':'127.0.0.1',
    'port':3306,#MySQL默认端口
    'user':'root',#mysql默认用户名
    'password':'tangao65267237',
    'db':'douban',#数据库
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor,
}
# 创建连接
con= pymysql.connect(**config)

# 执行sql语句
try:
    with con.cursor() as cursor:
        sql="select * from user"
        cursor.execute(sql)
        result=cursor.fetchall()
finally:
    con.close();
df=pd.DataFrame(result)#转换成DataFrame格式 df.head()

name_data=df['name'].tolist()#add_node
following_data=df['following_id']

relation_list=[]
for i in range(len(df)):
    a=df['name'][i]#取name
    if following_data[i]!='[]':
        b=following_data[i].split(",")#取following_id第一个数据并转换为list
        for j in range(len(b)):
            d=b[j].split("'")[1]
            if d in name_data:
                relation_list.append((a,d))#add_edge

import networkx as nx
G=nx.Graph()
G.clear()
G.add_nodes_from(name_data)
G.add_edges_from(relation_list)
print(G.number_of_nodes(),G.number_of_edges())
nx.write_gexf(G,'social_network.gexf')

