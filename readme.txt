#思路
#数据处理方式
#算法
#实现工具/语言
#a）	将1000名用户之间的社交关系用可视化工具展现出来。
    #mysql管理工具navicat(mac不支持sqlyog)，操作说明书http://www.navicat.com.cn/manual/pdf_manual/cn/navicat/mac_manual/navicat_mac_cs.pdf
    #运行sql导入数据——右键数据库连接——运行sql文件——选择sql文件——开始
    #mysql中读取数据
    #整理数据，去除following_id空值、筛选following_id中name列中的值
    #将数据生成gexf文件，方便导入gephi生成社交关系图（生成关系图方法https://gephi.org/tutorials/gephi-tutorial-quick_start.pdf）
#b）	根据该数据集提供的信息，设计一种电影推荐的算法，从1000部电影中选出合适的电影推荐给这1000名用户，同时说明推荐效果的评价方法并给出推荐效果得分。
    #movie表中有效字段（rate、directors、year、actors、type、countries）、user表中有效字段（rates、following_id）

#实验效果
#性能评价
#用英文

#豆瓣电影的个性化推荐
#a）	将1000名用户之间的社交关系用可视化工具展现出来。
#b）	根据该数据集提供的信息，设计一种电影推荐的算法，从1000部电影中选出合适的电影推荐给这1000名用户，同时说明推荐效果的评价方法并给出推荐效果得分。
#c）	加分项参考：自行设计爬虫上豆瓣网或其他网站（如百科或复旦大学知识工场网站http://kw.fudan.edu.cn/）爬取更多的数据，从新数据中抽取新的特征加入推荐系统，并充分证明推荐系统性能的提升（课程网站上的豆瓣爬虫源代码可供参考，文件名“豆瓣爬虫.rar”）。


#附：参考资料
#社会计算数据集：
#http://socialcomputing.asu.edu/
#
#可视化工具：
#Pajek:http://pajek.imfm.si
#D3: https://d3js.org
#NetworkX: https://networkx.readthedocs.io/en/stable/
#http://blog.sciencenet.cn/home.php?mod=space&uid=404069&do=blog&classid=141080&view=me&from=space
#Gephi: https://gephi.org/users/
#http://blog.csdn.net/zdw12242/article/details/8687644
#
#爬虫Cookie：http://blog.csdn.net/zhyh1435589631/article/details/51307915
#			 http://www.nowamagic.net/academy/detail/1302882
#
#爬虫防封技巧：http://blog.csdn.net/zhanghaipeng1989/article/details/40828377
#