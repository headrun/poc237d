''' This script is reilated to interpol it disobeys the robots.txt
'''
import datetime
import csv

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider

import xpaths_file 
import headers_file 

def extract_data(data, path, delem=''):
    return delem.join(i.strip() for i in data.xpath(path).extract() if i).strip().replace('\t', '').replace('\n', '').replace(';', ',')

class Interpol(BaseSpider):
    '''
    class starts
    '''
    name = 'interpol_new'
    start_domain = ['https://www.interpol.int']
    start_urls = ['https://www.interpol.int/notice/search/wanted']

    def __init__(self, keyword='', *args, **kwargs):
        super(Interpol, self).__init__(*args, **kwargs)
        self.keyword = keyword
	self.fields = ["url", "Family_name", "Criminal_Name", "sex", "Date_of_birth", "Place_of_birth", "Language_spoken", "Nationality", "Charges", "Regions_where_wanted"]
	oupf = open('Interpol-%s.csv'  % (str(datetime.date.today())), 'wb+')
	self.csv_file  = csv.writer(oupf)
        self.csv_file.writerow(self.fields)

    def parse(self, response):
        '''
        This function contains last pages_ navigations
        '''
        reference = response.url
        headers = headers_file.headers_list

        data = [('search', '1'), ('Name', self.keyword), ('Forename', ''), ('Nationality', ''), ('FreeText', ''), ('current_age_mini', '0'), ('current_age_maxi', '100'), ('Sex', ''), ('Eyes', ''), ('Hair', ''), ('RequestingCountry', ''), ('data', ''),]

        yield FormRequest('https://www.interpol.int/notice/search/wanted', callback=self.parse_next, headers=headers, formdata=data, meta={'reference':reference})

    def parse_next(self, response):
        '''
         This function contains required xpaths
        '''
        sel = Selector(response)
        reference = response.meta['reference']
        last_page_links = sel.xpath('//a[contains(@href, "/notice/search")]/@href').extract()
        for last_page in last_page_links:
            url = 'https://www.interpol.int' + last_page
            yield Request(url, self.parse_last_page_data, meta={'reference':reference})

    def parse_last_page_data(self, response):
        '''
        This function contains required xpaths
        '''
	sel = Selector(response)  
        reference = response.url
	family_name = extract_data(sel, xpaths_file.family_name_xpath)
	fore_name = extract_data(sel, xpaths_file.fore_name_xpath)
        fore_name = extract_data(sel, xpaths_file.fore_name_xpath)
        sex = extract_data(sel, xpaths_file.sex_xpath)
        date_of_birth = extract_data(sel, xpaths_file.date_of_birth_xpath)
        place_of_birth = extract_data(sel, xpaths_file.place_of_birth_xpath)
        language_spoken = extract_data(sel, xpaths_file.language_spoken_xpath)
        nationality = extract_data(sel, xpaths_file.nationality_xpath)
        charges = extract_data(sel, xpaths_file.charges_xpath)
        regions_where_wanted = extract_data(sel, xpaths_file.regions_where_wanted_xpath)
        csv_values = [reference, family_name.encode('utf8'), fore_name.encode('utf8'), sex, date_of_birth, place_of_birth, language_spoken, nationality, charges.encode('utf8'), regions_where_wanted.encode('utf8')]
        self.csv_file.writerow(csv_values)

