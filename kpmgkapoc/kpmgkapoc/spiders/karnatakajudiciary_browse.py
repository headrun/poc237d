# -*- coding: utf-8 -*-
import random
import scrapy
from scrapy.selector import Selector
from scrapy.http import FormRequest

from kpmgkapoc.utils import *
from kpmgkapoc.items import *
import karnatakajudiciary_xpaths as KX

class KarnatakajudiciaryBrowseSpider(scrapy.Spider):
    """ Spider name """
    name = 'karnatakajudiciary_browse'
    allowed_domains = ['karnatakajudiciary.kar.nic.in']
    start_urls = ['http://karnatakajudiciary.kar.nic.in/CaseStatus_PartyName.aspx/']
    custom_settings = {
                # specifies exported fields and order
                'FEED_EXPORT_FIELDS': ['Case_No', 'District', 'Data_Filed', 'Petitioner', 'Respondent', 'Pet_Advocate', 'Resp_Advocate', 'Sub_Type', 'Sub_SubType', 'Last_Action', 'Next_Hearing'],
                      }

    def __init__(self, *args, **kwargs):
        """ Initialize variables here """
        self.log = create_logger_obj(self.name)
        self.bench = kwargs.get('bench', 'Bengaluru Bench')
        self.resp_name = kwargs.get('resp', '')
        self.from_ = kwargs.get('from', '')
        self.to_ = kwargs.get('to', '')
        self.who = kwargs.get('who', '2')
        self.district = kwargs.get('dist', '0')
        self.case_type = kwargs.get('ctype', '0')

    def parse(self, response):
        """Start here"""
        sel = Selector(response)
        self.log.debug('Scrape started for %s in %s ' % (self.resp_name, self.bench))
        if self.resp_name == '':
            self.log.debug('Respondent or Petitioner name is needed')
            return
        if self.from_ == '' or self.to_ == '':
            self.log.debug('Filing - From Date or To Date is needed. -a from="dd/mm/yyyy" and -a to="dd/mm/yyyy"')
            return
        event_validation = ''.join(sel.xpath(KX.event_validation_xpath).extract())
        view_state = ''.join(sel.xpath(KX.view_state_xpath).extract())
        generator = ''.join(sel.xpath(KX.generator_xpath).extract())

        benches = sel.xpath(KX.benches_xpath)
        bench_dict = {}
        for bench in benches:
            key = ''.join(bench.xpath('./text()').extract()).strip()
            value = ''.join(bench.xpath('./@value').extract())
            bench_dict.update({key : value})

        bench_value = bench_dict[self.bench]

        petresdonts = sel.xpath(KX.petresdonts_xpath)
        petresdont_dict = {}
        for petresdont in petresdonts:
            key = ''.join(petresdont.xpath('./text()').extract())
            value = ''.join(petresdont.xpath('./@value').extract())
            petresdont_dict.update({key : value})

        petresdont_value = self.who
        if self.who != '2':
            petresdont_value = petresdont_dict[self.who]

        districts = sel.xpath(KX.districts_xpath)
        district_dict = {}
        for district in districts:
            key = ''.join(district.xpath('./text()').extract())
            value = ''.join(district.xpath('./@value').extract())
            district_dict.update({key : value})

        district_value = self.district
        if self.district != '0':
            district_value = district_dict[self.district]

        submitxy = [(random.randint(10, 90), random.randint(10, 90)) for i in range(10)]
        submitx, submity = random.choice(submitxy)

        form_data = {'__EVENTARGUMENT' : ''}
        form_data.update({'__EVENTTARGET' : ''})
        form_data.update({'__EVENTVALIDATION' : event_validation})
        form_data.update({'__VIEWSTATE' : view_state})
        form_data.update({'__VIEWSTATEGENERATOR' : generator})
        form_data.update({'ctl00$ContentPlaceHolder1$hfBench' : bench_value})
        form_data.update({'ctl00$ContentPlaceHolder1$ddlBench' : bench_value})
        form_data.update({'ctl00$ContentPlaceHolder1$ddlPetRespDont' : petresdont_value})
        form_data.update({'ctl00$ContentPlaceHolder1$ddlDistrict' : district_value})
        form_data.update({'ctl00$ContentPlaceHolder1$txtPartyName' : self.resp_name})
        form_data.update({'ctl00$ContentPlaceHolder1$txtFrmDate' : self.from_})
        form_data.update({'ctl00$ContentPlaceHolder1$txtToDate' : self.to_})
        form_data.update({'ctl00$ContentPlaceHolder1$hfdate' : self.to_})
        form_data.update({'ctl00$ContentPlaceHolder1$btnSubmit.x' : submitx})
        form_data.update({'ctl00$ContentPlaceHolder1$btnSubmit.y' : submity})

        url = 'http://karnatakajudiciary.kar.nic.in/CaseStatus_PartyName.aspx'
        yield FormRequest(url, callback=self.parse_next, formdata=form_data, dont_filter=True)

    def parse_next(self, response):
        """ After submit """
        sel = Selector(response)
        table_data = sel.xpath(KX.table_data_xpath)
        headers = ['Case_No', 'District', 'Data_Filed', 'Petitioner',\
                   'Respondent', 'Pet_Advocate', 'Resp_Advocate',\
                   'Sub_Type', 'Sub_SubType', 'Last_Action', 'Next_Hearing']
        if table_data:
            for i in table_data[1:]:
                _, case_no, _, district, data_filed, petitioner, respondent, advocate, resp_advocate, subtype, s_subtype, last_action, next_hearing = [i.strip() for i in i.xpath('.//td//text()').extract()]
                values = [case_no, district, data_filed, petitioner, respondent, advocate, resp_advocate, subtype, s_subtype, last_action, next_hearing]
                kpmg_item = KpmgkapocItem()
                for head, vals in zip(headers, values):
                    kpmg_item.update({head : vals})
                yield kpmg_item
            

