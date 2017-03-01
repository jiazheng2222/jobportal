# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings

SETTINGS = get_project_settings()

class JiujikPipeline(object):

    def __init__(self):

        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            db = SETTINGS['DB_DB'],
                                            user = SETTINGS['DB_USER'],
                                            passwd = SETTINGS['DB_PASSWD'],
                                            host = SETTINGS['DB_HOST'],
                                            port = SETTINGS['DB_PORT'],
                                            charset = 'utf8',
                                            use_unicode = False
                                            )

    def __del__(self):
        self.dbpool.close()

    def process_item(self, item, spider):
    #    self.insert_data(item, self.insert_sql)
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self,tx,item):
        tx.execute('insert into industry (name, link) \
            values (%s, %s)', (item['Name'],item['Link']))

    