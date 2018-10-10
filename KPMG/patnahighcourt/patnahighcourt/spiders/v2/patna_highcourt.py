import re
import random
import csv

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest

import xpaths_file
import configure 

DEFAULT_HEADERS = configure.DEFAULT_HEADERS_LIST
 
def extract_data(sel, xpath_, delim=''):
    return delim.join(sel.xpath(xpath_).extract()).strip()

class PatnaHighCourt(Spider):
    name = 'patna_highcourt'
    start_urls = []

    def __init__(self, *args, **kwargs):
        self.keyword = kwargs.get('keyword', '')
        self.year = kwargs.get('year', '')
        self.excel_file_name = 'patna_data_'+self.keyword.replace(' ', '_')+'_'+self.year.strip()+'.csv'
        self.oupf = open(self.excel_file_name, 'w+')
        self.todays_excel_file = csv.writer(self.oupf) 
        court_headers = ['Token Number', 'Status', 'Petitioner', 'Respondent', 'Date of Filing', 'Case Number']
        self.todays_excel_file.writerow(court_headers) 

    def start_requests(self):
        url = 'http://patnahighcourt.gov.in/CaseSeachByName.aspx'
        yield Request(url, callback=self.parse, headers=DEFAULT_HEADERS)

    def parse(self, response):
        sel = Selector(response)
        cookie = response.headers.getlist('Set-Cookie')
        cookies = {}
        for i in cookie:
            data = i.split(';')[0]
            if data:
                try: key, val = data.split('=', 1)
                except: continue
                cookies.update({key.strip():val.strip()})
            headers = configure.headers_list
 			
        event_target = extract_data(sel, xpaths_file.event_target_list)
        event_argument = extract_data(sel, xpaths_file.event_argument_list)
        view_state = extract_data(sel, xpaths_file.view_state_list)
        event_validation = extract_data(sel, xpaths_file.event_validation_list)
        view_state_encrypted = extract_data(sel, xpaths_file.view_state_encrypted_list)

        data = [
            ('__EVENTTARGET', event_target),
            ('__EVENTARGUMENT', event_argument),
            ('__VIEWSTATE', view_state),
            ('__SCROLLPOSITIONX', '0'),
            ('__SCROLLPOSITIONY', '0'),
            ('__VIEWSTATEENCRYPTED', view_state_encrypted),
            ('__EVENTVALIDATION', event_validation),
            ('ctl00$MainContent$ddlCaseType', '0'),
            ('ctl00$MainContent$txtName', self.keyword),
            ('ctl00$MainContent$txtYear', str(self.year).strip()),
            ('ctl00$MainContent$txtCaptcha', cookies.get('CaptchaImageText', '')),
            ('ctl00$MainContent$btnSeach', 'Show'),
        ]
        basic_search_url = configure.basic_search_url_list
	yield FormRequest(basic_search_url, callback=self.parse_results, headers=headers, formdata=data, cookies=cookies, meta={'req_cookie':cookies})

    def parse_results(self, response):
        sel = Selector(response)
        cookies = response.meta.get('req_cookie', {})
        view_state_result = extract_data(sel, xpaths_file.view_state_result_list)
        view_state_encrypted_result = extract_data(sel, xpaths_file.view_state_encrypted_result_list)
        event_validation_result = extract_data(sel, xpaths_file.event_validation_result_list)
        nodes = sel.xpath(xpaths_file.nodes_list)

        for node in nodes:
            case_url = extract_data(node, xpaths_file.case_url_list)
            case_year = extract_data(node, xpaths_file.case_year_list)
            token_no = extract_data(node, xpaths_file.token_no_list)
            petitioner_name = extract_data(node, xpaths_file.petitioner_name_list)
            respondent_name = extract_data(node, xpaths_file.respondent_name_list)
            filing_date = extract_data(node, xpaths_file.filing_date_list)
            pet_advocate = extract_data(node, xpaths_file.pet_advocate_list)

            if case_url:
                values = re.findall("javascript:__doPostBack\('(.*)','(.*)'\)", case_url)
                if values:
                    ev_target, ev_argument = values[0]
                    screen_y = random.choice(range(0, 100))

                headers = configure.headers_results
                data = [
	                   ('__EVENTTARGET', ev_target),
		                  ('__EVENTARGUMENT', ev_argument),
		                  ('__VIEWSTATE', view_state_result),
		                  ('__SCROLLPOSITIONX', '0'),
		                  ('__SCROLLPOSITIONY', '181'),
		                  ('__VIEWSTATEENCRYPTED', view_state_encrypted_result),
	                   ('__EVENTVALIDATION', event_validation_result),
		                  ('ctl00$MainContent$ddlCaseType', '0'),
		                  ('ctl00$MainContent$txtName', ''),
		                  ('ctl00$MainContent$txtYear', ''),
		                  ('ctl00$MainContent$txtCaptcha', ''),
		]
                base_url = 'http://patnahighcourt.gov.in/CaseSeachByName.aspx'
                yield FormRequest(base_url, self.parse_eachcase, headers=headers, formdata=data, cookies=cookies)		


    def parse_eachcase(self, response):
        sel = Selector(response)
        token_number = extract_data(sel, xpaths_file.token_number_xpath)
        case_status = extract_data(sel, xpaths_file.case_status_xpath)
        petitioner = extract_data(sel, xpaths_file.petitioner_xpath)
        respondent = extract_data(sel, xpaths_file.respondent_xpath)
        date_filing = extract_data(sel, xpaths_file.date_filing_xpath)
        case_no = extract_data(sel, xpaths_file.case_no_xpath)
        values = [token_number, case_status, petitioner, respondent, date_filing, case_no]
        self.todays_excel_file.writerow(values)
