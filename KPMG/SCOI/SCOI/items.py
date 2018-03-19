# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field

class SCOIItem(Item): 
    ref_url = Field()
    partyName = Field()
    PartyYear = Field()
    PartyStatus = Field()
    diary_no =Field()
    case_no = Field()
    present_last = Field()
    status = Field()
    listed_on = Field()
    admitted = Field()
    category = Field()
    act = Field()
    petitioner = Field()
    respondent = Field()
    pet_advocate = Field()
    resp_advocate = Field()
    u_section = Field()
    case_number = Field()
    #pass

