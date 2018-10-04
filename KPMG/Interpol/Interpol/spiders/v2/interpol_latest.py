''' This script is reilated to interpol it disobeys the robots.txt
'''
import datetime
import os
import csv

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider

from Interpol.spiders.xpaths_file import *
from Interpol.spiders.headers_file import *

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
        self.filename = "interpol%s.csv" % (str(datetime.datetime.now().date()))
        self.csv_file = self.is_path_file_name(self.filename)
        self.fields = ["url", "Family_name", "Criminal_Name", "sex", "Date_of_birth", "Place_of_birth", "Language_spoken", "Nationality", "Charges", "Regions_where_wanted"]
        self.csv_file.writerow(self.fields)

    def is_path_file_name(self, excel_file_name):
        '''
        This function contains csv_file generation
        '''
        if os.path.isfile(excel_file_name):
            os.system('rm%s' % excel_file_name)
        oupf = open(excel_file_name, 'ab+')
        todays_excel_file = csv.writer(oupf)
        return todays_excel_file

    def parse(self, response):
        '''
        This function contains last pages_ navigations
        '''
        reference = response.url
        headers = headers_list

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
        family_name = ''.join(sel.xpath(family_name_xpath).extract())
        fore_name = ''.join(sel.xpath(fore_name_xpath).extract())
        sex = ''.join(sel.xpath(sex_xpath).extract())
        date_of_birth = ''.join(sel.xpath(date_of_birth_xpath).extract())
        place_of_birth = ''.join(sel.xpath(place_of_birth_xpath).extract())
        language_spoken = ''.join(sel.xpath(language_spoken_xpath).extract()).replace('\t', '').replace('\n', '')
        nationality = ''.join(sel.xpath(nationality_xpath).extract()).replace('\t', '').replace('\n', '')
        charges = ''.join(sel.xpath(charges_xpath).extract()).replace(';', ',')
        regions_where_wanted = str(''.join(sel.xpath(regions_where_wanted_xpath).extract()))
        csv_values = [reference, family_name.encode('utf8'), fore_name.encode('utf8'), sex, date_of_birth, place_of_birth, language_spoken, nationality, charges.encode('utf8'), regions_where_wanted.encode('utf8')]
        self.csv_file.writerow(csv_values)

