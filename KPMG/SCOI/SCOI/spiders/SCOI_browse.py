from scrapy.http import  Request, FormRequest
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from SCOI.items import *
import re
import requests
import json
import urllib 


class SCOI(BaseSpider):
    name = 'SCOI_browse'
    start_urls = ['http://www.supremecourtofindia.nic.in/case-status']

    def __init__(self,party_name = '', party_year = '', party_status = '', **kwargs):
        super(SCOI, self).__init__(**kwargs)
        self.party_name = party_name
        self.party_year = party_year
        self.party_status = party_status

        self.data = [ 
          ('PartyType', ''),
          ('PartyName', self.party_name), 
          ('PartyYear', self.party_year), 
          ('PartyStatus', self.party_status),
          ('page', '1'),
        ]

    def parse(self, response):
        yield FormRequest('http://www.supremecourtofindia.nic.in/php/getPartyDetails.php', callback=self.parse_next, formdata = self.data)

    def parse_next(self, response):
        sel = Selector(response)
        nodes_cases = sel.xpath('//tbody/tr[@valign="top"][@bgcolor][td[@align="center"]]')
        form_data = response.meta.get('formdata', {})
        for nd in nodes_cases:
                case_number = ' '.join(nd.xpath('.//td[@align="center"]//text()').extract())
                case_url = ' '.join(nd.xpath('.//a[*[@class="pet"]]/@href').extract())
                if case_url:
                    case_url = 'http://www.supremecourtofindia.nic.in/'+ case_url
                    yield Request(case_url, callback = self.parse_case_url, meta = {"case_no":case_number})
        next_page = ' '.join(sel.xpath('//li[@class="active"][contains(text(), "Next")]/@p').extract()).strip()
        if next_page:
            self.data.pop()
            page = ('page', '%s' %next_page)
            self.data.append(page)
            print self.data
            yield FormRequest('http://www.supremecourtofindia.nic.in/php/getPartyDetails.php', callback=self.parse_next, formdata = self.data, meta = {"formdata":self.data}) 
            
    def parse_case_url(self, response):
        sel = Selector(response)
        records = sel.xpath('//div[h4[a[contains(text(),"Case Details")]]]/following-sibling::div')
        diary_no = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Diary No.")]]//td[not(@*)]//text()').extract()))
        case_no = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Case No.")]]//td[not(@*)]//text()').extract()))
        present_last = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Present/Last Listed On")]]//text()').extract()))
        status = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Status/Stage")]]//text()').extract()))
        listed_on = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Tentatively case may be listed on ")]]//text()').extract()))
        admitted = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Admitted")]]//text()').extract()))
        category = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Category")]]//text()').extract()))
        act = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Act")]]//td[not(@*)]//text()').extract()))
        petitioner = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Petitioner(s)")]]//td[not(@*)]//text()').extract()))
        respondent = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Respondent(s)")]]//td[not(@*)]//text()').extract()))
        pet_advocate = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Pet. Advocate(s)")]]//td[not(@*)]//text()').extract()))
        resp_advocate = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "Resp. Advocate(s)")]]//td[not(@*)]//text()').extract()))
        u_section = self.xcode(' '.join(records.xpath('.//tr[td[contains(text(), "U/Section")]]//td[not(@*)]//text()').extract()))
        SCOI = SCOIItem()
        SCOI['ref_url'] = response.url
        SCOI['partyName'] =  self.party_name
        SCOI['PartyYear'] = self.party_year
        SCOI['PartyStatus'] = self.party_status
        SCOI['diary_no'] = diary_no 
        SCOI['case_no'] = case_no 
        SCOI['present_last'] = present_last 
        SCOI['status'] = status 
        SCOI['listed_on'] = listed_on 
        SCOI['admitted'] = admitted 
        SCOI['category'] = category 
        SCOI['act'] = act 
        SCOI['petitioner'] = petitioner 
        SCOI['respondent'] = respondent 
        SCOI['pet_advocate'] = pet_advocate 
        SCOI['resp_advocate'] = resp_advocate 
        SCOI['u_section'] = u_section 
        SCOI['case_number'] = response.meta['case_no']
        if SCOI['case_number']:
            yield SCOI
   
    def xcode(self, text, encoding='utf8', mode='strict'):
        return text.encode(encoding, mode).replace('\xc2\xa0\xc2\xa0','').replace('\n','').replace('\xc2\xa0\xc2\xa050','').replace('\xc2\xa0\xc2\xa02','').replace('\xc2\xa0\xc2\xa03','').replace('\xc2\xa0\xc2\xa01','') if isinstance(text, unicode) else text 


