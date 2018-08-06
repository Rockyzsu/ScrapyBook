# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from twisted.enterprise import adbapi


class BookPipeline(object):
    review_rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    def process_item(self, item, spider):
        rating = item.get('review_rating')
        if rating:
            item['review_rating'] = self.review_rating_map[rating]

        return item


class MySQLPipeline:
    def open_spider(self, spider):
        db = spider.setting.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.setting.get('MYSQL_HOST', 'localhost')
        port = spider.setting.get('MYSQL_PORT', 3306)
        user = spider.setting.get('MYSQL_USER', 'root')
        passwd = spider.setting.get('MYSQL_PASSWORD', '123456')

        self.dbpool = adbapi.ConnectionPool('MySQLdb', host=host, port=port,
                                            db=db, user=user, passwd=passwd, charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close()

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)

        return item

    def insert_db(self, tx, item):
        values = (
            item['upc'],
            item['name'],
            item['price'],
            item['review_rating'],
            item['review_num'],
            item['stock'],
        )

        sql = 'INSERT INTO books VALUES (%s, %s, %s, %s, %s, %s)'
        tx.execute(sql, values)