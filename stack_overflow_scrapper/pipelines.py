# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector

class StackOverflowScrapperPipeline(object):
    def __init__(self):
        self.db = mysql.connector.connect(
            host="remotemysql.com",
            user="HXxmuy2MNm",
            password="m1siNFwULh",
            database="HXxmuy2MNm",
        )
        self.cursor = self.db.cursor()

        self.cursor.execute('DROP TABLE IF EXISTS TAGS')
        self.cursor.execute('DROP TABLE IF EXISTS QUESTION')
        self.cursor.execute('''
            CREATE TABLE QUESTION(
                ID INTEGER AUTO_INCREMENT PRIMARY KEY,
                TITLE VARCHAR(500),
                DESCRIPTION VARCHAR(10000),
                ASKED_BY VARCHAR(100),
                VIEWS VARCHAR(20),
                VOTES VARCHAR(20),
                ANSWERS VARCHAR(20)
            )
            ''')

        self.cursor.execute('''
            CREATE TABLE TAGS(
                ID INTEGER AUTO_INCREMENT PRIMARY KEY,
                QUESTION_ID INTEGER,
                TAG VARCHAR(100),
                FOREIGN KEY (QUESTION_ID) REFERENCES QUESTION(ID)
            )
        ''')


    def insert_question(self, item):
        title = item['title'][0]
        description = item['description'][0]
        asked_by = item['asked_by'][0]
        views = item['views'][0]
        votes = item['votes'][0]
        answers = item['answers'][0]
        tags = item['tags']
        sql = '''
            INSERT INTO QUESTION(TITLE, DESCRIPTION, ASKED_BY, VIEWS, VOTES, ANSWERS)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        values = (title, description, asked_by, views, votes, answers)

        self.cursor.execute(sql, values)

        self.db.commit()

        sql = '''
            INSERT INTO TAGS(QUESTION_ID, TAG)
            VALUES (%s, %s)
        '''
        id = self.cursor.lastrowid

        for tag in tags:
            values = (id, tag)
            self.cursor.execute(sql, values)
            self.db.commit()

    def process_item(self, item, spider):
        self.insert_question(item)
        return item
