# coding:utf-8
# references:https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
"""爬虫管道：用于保存数据到mysql"""
import mysql.connector


class SaveDataToMySqlDbPipeline(object):
    """
    保存数据到数据库管道
    """
    config = {'user': 'root', 'password': '1234ABcd_', 'host': '127.0.0.1'}

    def __init__(self):
        self.cnx = mysql.connector.connect(**self.config)
        self.cursor = self.cnx.cursor()
        dbname = 'spider'
        create_database_sql = 'create database if not exists %s' % dbname
        self.cursor.execute(create_database_sql)
        self.cnx.database = dbname
        create_table_sql = '''create table if not exists douban_book
        (id smallint primary key auto_increment,
        name varchar(20) not null,
        author varchar(100) not null,
        publisher varchar(50) not null,
        publish_date varchar(10) not null,
        vote float unsigned not null,
        rank smallint ,
        url varchar(100) not null)'''
        self.cursor.execute(create_table_sql)
        self.cnx.commit()

    def process_item(self, item, spider):
        """
        处理bookitem，保存到数据库
        """
        add_book = ("insert into douban_book"
                    "(name,author,publisher,publish_date,vote,rank,url)"
                    "values(%s,%s,%s,%s,%s,%s,%s)")
        book = (item['name'], item['author'], item['publisher'],
                item['publish_date'], item['vote'], item['rank'], item['url'])
        self.cursor.execute(add_book, book)
        self.cnx.commit()
        return item

    def spider_closed(self, spider):
        """
        爬虫关闭时，关闭游标关闭连接
        """
        self.cursor.close()
        self.cnx.close()
