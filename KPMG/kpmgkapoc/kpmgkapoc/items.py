# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class KpmgkapocItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Case_No = Field()
    District = Field()
    Data_Filed = Field()
    Petitioner = Field()
    Respondent = Field()
    Pet_Advocate = Field()
    Resp_Advocate = Field()
    Sub_Type = Field()
    Sub_SubType = Field()
    Last_Action = Field()
    Next_Hearing = Field()
    pass
