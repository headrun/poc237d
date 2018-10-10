import datetime
import os
import csv
import re
import math

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import configure

class Fbi(Spider):
    name = 'fbi_latest'
    start_urls = configure.start_urls_list

    def __init__(self,*args, **kwargs):
	super(Fbi, self).__init__(*args, **kwargs)
	self.fields = configure.fields_list
	oupf = open('fbi-%s.csv'  % (str(datetime.date.today())), 'wb+')
        self.csv_file = csv.writer(oupf) 
	self.csv_file.writerow(self.fields)

    def parse(self, response):
                sel = Selector(response)
                category_urls = sel.xpath(configure.category_urls_list).extract()
                for each in category_urls:
                        yield Request(each, callback = self.parse_next)

    def parse_next(self, response):
                sel = Selector(response)
                url = response.url
		if 'terrorism' in url:
		        per_page_results = sel.xpath(configure.per_page_results_terrorism).extract()
                        data = re.findall('\d+', per_page_results[0])
                        total_pages = data[2]
                        results_per_page = data[1]
                        page_number = float(total_pages)/float(results_per_page)
                        no_of_pages = int(math.ceil(page_number))
                        for_need = no_of_pages + 1
                        y = range(1,for_need)
                        complete_url = configure.complete_url_terrorism
                        for x in y:
                                terroism_url = complete_url+str(x)
                                yield Request(terroism_url, callback=self.parse_allnames)

		if 'vicap' in url:
                        per_page_results = sel.xpath(configure.per_page_results_vicap).extract()
                        data = re.findall('\d+', per_page_results[0])
                        total_pages = data[2]
                        results_per_page = data[1]
                        page_number = float(total_pages)/float(results_per_page)
                        no_of_pages = int(math.ceil(page_number))
                        for_need = no_of_pages + 1
                        y = range(1,for_need)
                        complete_url = configure.complete_url_vicap
                        for x in y:
                                seeking_url = complete_url+str(x)
                                yield Request(seeking_url, callback=self.parse_allnames)

		if 'seeking-information' in url:
                        per_page_results = sel.xpath(configure.per_page_results_seeking_information).extract()
                        data = re.findall('\d+', per_page_results[0])
                        total_pages = data[2]
                        results_per_page = data[1]
                        page_number = float(total_pages)/float(results_per_page)
                        no_of_pages = int(math.ceil(page_number))
                        for_need = no_of_pages + 1
                        y = range(1,for_need)
                        complete_url = configure.complete_url_seeking_information
                        for x in y:
                                seeking_url = complete_url+str(x)
                                yield Request(seeking_url, callback=self.parse_allnames)

		if 'wanted/kidnap' in url:
                        per_page_results = sel.xpath(configure.per_page_results_wanted_kidnap).extract()
                        data = re.findall('\d+', per_page_results[0])
                        total_pages = data[2]
                        results_per_page = data[1]
                        page_number = float(total_pages)/float(results_per_page)
                        no_of_pages = int(math.ceil(page_number))
                        for_need = no_of_pages + 1
                        y = range(1,for_need)
                        complete_url = configure.complete_url_wanted_kidnap
                        for x in y:
                                kidnap_url = complete_url+str(x)
                                yield Request(kidnap_url, callback=self.parse_allnames)

		if 'topten' in url:
                        name_url_nodes = sel.xpath(configure.name_url_nodes_topten)
                        for node in name_url_nodes:
                                name = ''.join(node.xpath(configure.name_topten).extract())
                                each_url = ''.join(node.xpath(configure.each_url_topten).extract())
                                yield Request(each_url, callback=self.parse_detail, meta = {'name':name})
		
		if 'fugitives' in url:
                        per_page_results = sel.xpath(configure.per_page_results_fugitives).extract()
                        data = re.findall('\d+', per_page_results[0])
                        total_pages = data[2]
                        results_per_page = data[1]
                        page_number = float(total_pages)/float(results_per_page)
                        no_of_pages = int(math.ceil(page_number))
                        for_need = no_of_pages + 1
                        y = range(1,for_need)
                        complete_url = configure.complete_url_fugitives
                        for x in y:
                                fugitives_url = complete_url+str(x)
                                yield Request(fugitives_url, callback=self.parse_allnames)

		if 'parental-kidnappings' in url:
                        name_url_nodes = sel.xpath(configure.name_url_nodes_parental_kidnappings)
                        for node in name_url_nodes:
                                name = ''.join(node.xpath(configure.name_parental_kidnappings).extract())
                                each_url = ''.join(node.xpath(configure.each_url_parental_kidnappings).extract())
                                yield Request(each_url, callback=self.parse_detail, meta = {'name':name})

		if 'bank-robbers' in url:
			name_url_nodes = sel.xpath(configure.name_url_nodes_bank_robbers)
                	for node in name_url_nodes:
                        	name = ''.join(node.xpath(configure.name_bank_robbers).extract())
                        	each_url = ''.join(node.xpath(configure.each_url_bank_robbers).extract())
                        	yield Request(each_url, callback=self.parse_detail,meta = {'name':name})
	
		if 'ecap' in url:
                        name_url_nodes = sel.xpath(configure.name_url_nodes_ecap)
                        for node in name_url_nodes:
                                name = ''.join(node.xpath(configure.name_ecap).extract())
                                each_url = ''.join(node.xpath(configure.each_url_ecap).extract())
                                yield Request(each_url, callback=self.parse_detail, meta = {'name':name})

    def parse_allnames(self, response):
                sel = Selector(response)
		name_url_nodes = sel.xpath(configure.name_url_nodes_all_names)
                for node in name_url_nodes:
                        name = ''.join(node.xpath(configure.name_all_names).extract())
			if not name: name = ''.join(node.xpath(configure.name_allnames).extract())
                        each_url = ''.join(node.xpath(configure.each_url_all_names).extract())
			if not each_url: each_url = ''.join(node.xpath(configure.each_url_allnames).extract())
                        yield Request(each_url, callback=self.parse_detail,meta = {'name':name})

    def parse_detail(self, response):
        name = response.meta.get('name','')
        url = response.url
        sel = Selector(response)
        aliases = ''.join(sel.xpath(configure.aliases_detail).extract())
        remarks = ''.join(sel.xpath(configure.remarks_detail).extract())
        caution = ''.join(sel.xpath(configure.caution_detail).extract())
	nationality = ''.join(sel.xpath(configure.nationality_detail).extract())
        csv_values = [name, url, aliases, remarks, caution, nationality]
        self.csv_file.writerow(csv_values)

