import pandas as pd
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
con= pymysql.connect(**config)#字典形式

# 执行sql语句
try:
    with con.cursor() as cursor:
        sql="select * from user"
        cursor.execute(sql)
        result=cursor.fetchall()
finally:
    con.close();
df_user=pd.DataFrame(result)

# 创建连接
con= pymysql.connect(**config)

# 执行sql语句
try:
    with con.cursor() as cursor:
        sql="select * from movie"
        cursor.execute(sql)
        result=cursor.fetchall()
finally:
    con.close();
df_movie=pd.DataFrame(result)

df_user=df_user.filter(items=['name','rates','following_id'],axis=1)
df_movie=df_movie.filter(items=['rate','title','id','directors','year','actors','type','countries'])




for i in range(len(df_user['following_id'])):
    tmp_list = []
    if df_user['following_id'].iloc[i]!='[]' :
        a=df_user['following_id'].iloc[i].split(",")
        for j in range(len(a)):
            b=a[j].split("'")[1]
            if b in df_user['name'].values:
                tmp_list.append(b)
    df_user['following_id'].iloc[i]=tmp_list



df_user=df_user.drop('rates',axis=1).join(df_user['rates'].str.split(",",expand=True).stack().reset_index(level=1,drop=True).rename('rates'))
df_user['user_movie_id']=df_user['rates'].str.split("'").str[1]
df_user['movie_score']=df_user['rates'].str.split("'").str[3]
df_user=df_user.drop('rates',axis=1)

#df_user=df_user.drop('following_id',axis=1).join(df_user['following_id'].str.split(",",expand=True).stack().reset_index(level=1,drop=True).rename('following_id'))
print(df_user['following_id'][:10])
print(df_user['following_id'][:10].str.split())



countries_dummies=pd.get_dummies(df_movie['countries'])
df_movie=df_movie.join(countries_dummies)
df_movie.drop('countries',axis=1,inplace=True)

df_movie=df_movie.drop('type',axis=1).join(df_movie['type'].str.split(",",expand=True).stack().reset_index(level=1,drop=True).rename('type'))
type_dummies=pd.get_dummies(df_movie['type'])
df_movie=df_movie.join(type_dummies)
df_movie.drop('type',axis=1,inplace=True)
df_movie.drop(['directors','actors'],axis=1,inplace=True)
df_movie=df_movie.reset_index()


#df_user.to_csv("user.csv")
#df_movie.to_csv("movie.csv")











