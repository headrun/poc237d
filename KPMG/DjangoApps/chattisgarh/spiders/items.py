# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class ChhattisgarhpocItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DataItem(Item):
	
	case_number  		= Field()
	keyword			= Field()
	year			= Field()
	petitioner   		= Field()
	petitioner_advocate 	= Field()
	respondent  		= Field()
	respondent_advocate 	= Field()
	case_status  		= Field()
	decision_date 		= Field()
