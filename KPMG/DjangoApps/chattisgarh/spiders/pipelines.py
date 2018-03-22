# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from items import DataItem

class ChhattisgarhpocPipeline(object):
    #def process_item(self, item, spider):
    #    return item

    def __init__(self):
    	self.conn = MySQLdb.connect(host="localhost", user = "root", passwd='root', db = "HC_CHATTISGARH", charset="utf8", use_unicode=True)
        self.cur = self.conn.cursor()
    def process_item(self, item, spider):
	#import pdb;pdb.set_trace()
	if isinstance(item, DataItem):
		#import pdb;pdb.set_trace()
		keyword   = item.get('keyword', '')
		year      = item.get('year', '')
		case_number =   item.get('case_number', '') 
		petitioner =    item.get('petitioner', '')
		petitioner_advocate = item.get('petitioner_advocate', '')
		respondent  = item.get('respondent', '')
		respondent_advocate = item.get('respondent_advocate', '')
		case_status = item.get('case_status', '')
		decision_date = item.get('decision_date', '')
		query = "insert into case_details(case_number, keyword, year, petitioner, petitioner_advocate, respondent, respondent_advocate, case_status, decision_date, created_at, modified_at) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()) on duplicate key update modified_at=now(), case_status=%s, decision_date=%s"
		values = (case_number, keyword, year, petitioner, petitioner_advocate, respondent, respondent_advocate, case_status, decision_date, case_status, decision_date)
		self.cur.execute(query, values)
		self.conn.commit()		
		
