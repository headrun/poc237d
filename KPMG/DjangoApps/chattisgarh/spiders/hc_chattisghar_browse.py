import re
import csv
import datetime
from scrapy.http import Request, FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector
from xpaths_file import *
from chhattisgarhpoc.items import DataItem
from datetime import datetime


def normalize(text):
    return clean(compact(xcode(text)))

def clean(text):
    if not text: return text 

    value = text 
    value = re.sub("&amp;", "&", value)
    value = re.sub("&lt;", "<", value)
    value = re.sub("&gt;", ">", value)
    value = re.sub("&quot;", '"', value)
    value = re.sub("&apos;", "'", value)

    return value

def compact(text, level=0):
    if text is None: return ''

    if level == 0:
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")

    compacted = re.sub("\s\s(?m)", " ", text)
    if compacted != text:
        compacted = compact(compacted, level+1)

    return compacted.strip()

def xcode(text, encoding='utf8', mode='strict'):
    return text.encode(encoding, mode) if isinstance(text, unicode) else text


def extract_data(data, path, delem=''):
    return delem.join(i.strip() for i in data.xpath(path).extract() if i).strip()

class HCChhattisghar(Spider):
    name = 'chhattisghar_browse'
    start_urls = ["http://services.ecourts.gov.in/ecourtindiaHC/cases/ki_petres.php?state_cd=18&dist_cd=1&stateNm=Chhattisgarh#"]
    row_count = 1
    headers = {'Pragma': 'no-cache',
               'Origin': 'http://services.ecourts.gov.in',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'en-GB,en-US;q=0.8,en;q=0.6',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': '*/*',
               'Cache-Control': 'no-cache',
               'Referer': 'http://services.ecourts.gov.in/ecourtindiaHC/cases/ki_petres.php?state_cd=18&dist_cd=1&stateNm=Chhattisgarh',
               'Connection': 'keep-alive'}

    def __init__(self, *args, **kwargs):
        self.word = kwargs.get('word', '')
        self.year = kwargs.get('year', '2017')
	#import pdb;pdb.set_trace()
        #self.path = kwargs.get('path', '')
        #if self.path:self.path += '/'
        #self.excel_file_name = self.path + '%s_%s_%s_hc_chhattisgarh.csv'%(self.word.replace(' ', '-'), self.year, str(datetime.datetime.now().date()))
        #self.oupf = open(self.excel_file_name, 'w+')
        #self.todays_excel_file = csv.writer(self.oupf) 
        #court_headers = ['Case number', 'Petitioner', 'Petitioner Advocate', 'Respondent', 'Respondent Advocate', 'Case status', 'Decision Date']
        #self.todays_excel_file.writerow(court_headers)
        self.adv_regex = re.compile(r'Advocate(.*)')
        self.add_regex = re.compile(r'Address(.*)')

    def parse(self, response):
	sel = Selector(response)
        headers = response.headers
        sid = sel.xpath(csrf_xpath).extract()
        sessionid = headers.get('Set-Cookie', '')
        sessionid = ''.join(re.findall('PHPSESSID=(.*); path', sessionid))
        data = [('__csrf_magic', ''.join(sid)), ('undefined', '')]
        url = 'http://services.ecourts.gov.in/ecourtindiaHC/cases/audiocaptcha.php'
        yield FormRequest(url, callback=self.parse_captcha, formdata=data, headers=self.headers, method="POST", meta={'sid':''.join(sid), 'sessionid':sessionid})

    def parse_captcha(self, response):
        captcha = response.body
        sid = response.meta['sid']
        sessionid = response.meta['sessionid']
        cookies = {'PHPSESSID': sessionid}
        data = [('__csrf_magic', sid),
                ('action_code', 'showRecords'),
                ('state_code', '18'),
                ('dist_code', '1'),
                ('f', 'Both'),
                ('petres_name', self.word),
                ('rgyear', self.year),
                ('captcha', captcha)]
        url = 'http://services.ecourts.gov.in/ecourtindiaHC/cases/ki_petres_qry.php'
        yield FormRequest(url, callback=self.parse_data, cookies=cookies, formdata=data, headers=self.headers, method="POST", meta={'sid':sid, 'sessionid':sessionid})

    def parse_data(self, response):
	sid = response.meta['sid']
        sessionid = response.meta['sessionid']
                
        rows = [e for e in response.body.split('##') if e.strip()]
        
        for row in rows:
            columns = row.split('~')
            case_no = columns[0].replace('\xef\xbb\xbf', '').strip()
            cino = columns[3].strip()
            
            cookies = {'PHPSESSID': sessionid}

            data = [
                ('__csrf_magic', sid),
                ('court_code', ''),
                ('state_code', '18'),
                ('dist_code', '1'),
                ('case_no', case_no),
                ('cino', cino),
                ('appFlag', ''),
                    ] 
            
            url = "http://services.ecourts.gov.in/ecourtindiaHC/cases/o_civil_case_history.php"
            yield FormRequest(url, callback=self.parse_view, cookies=cookies, formdata=data, headers=self.headers, method="POST", meta={'sid':sid, 'sessionid':sessionid})
	
    def parse_view(self, response):
	record = DataItem()
        sel = Selector(text=normalize(response.body))  
        pet_details  = extract_data(sel, pet_adv_xpath, '\n')
        resp_details = extract_data(sel, resp_adv_xpath, '\n')
        case_num = self.clean_text(extract_data(sel, case_num_xpath), ':').split('/')[0]
        
        pet_adv, pet_add = '', ''
        resp_adv, resp_add = '', ''
        peti, respi = '', ''
        status = ''
        if pet_details:
            peti = self.clean_text(pet_details.split('\n')[0].strip().split('1)')[-1], ',')
            pet_adv = self.clean_text(self.clean_text(''.join(re.findall(self.adv_regex, pet_details)), '-').replace('Advocate', ''), '-')
            pet_add = self.clean_text(''.join(re.findall(self.add_regex, pet_details)), '-')
        if resp_details:
            respi = self.clean_text(resp_details.split('\n')[0].strip().split('1)')[-1], ',')
            resp_adv = self.clean_text(self.clean_text(''.join(re.findall(self.adv_regex, resp_details)), '-').replace('Advocate', ''), '-')
            resp_add = self.clean_text(''.join(re.findall(self.add_regex, resp_details)), '-')

        status = self.clean_text(extract_data(sel, status_xpath), ':')

        if not status:
            status = self.clean_text(extract_data(sel, alt_status_xpath), ':')

        decision_date = self.clean_text(extract_data(sel, decision_dt_xpath), ':')
        court_values = [case_num, peti, pet_adv, respi, resp_adv, status, decision_date]
        court_values = [self.clean_text(e.replace(u'\xa0', ' ').replace(',,', ',').strip(), ',') for e in court_values]
        
	record['case_number'] = court_values[0]
	record['petitioner'] = court_values[1]
	record['petitioner_advocate'] = court_values[2]
	record['respondent']  = court_values[3]
	record['respondent_advocate'] = court_values[4]
	record['case_status'] = court_values[5]
	record['keyword'] = self.word
	record['year'] = self.year
	#import pdb;pdb.set_trace()
	if decision_date.strip('-').strip():
		#import pdb;pdb.set_trace()
		date = decision_date.strip('-').strip()
		try:
			date = str(datetime.strptime(date.replace('th ', ' ').replace('nd ',' ').strip(), '%d %B %Y'))
		except:
			date = '0000-00-00'
	else:date = '0000-00-00'
	record['decision_date'] = date
	
        #self.todays_excel_file.writerow(court_values)
       	yield record
    def clean_text(self, text, param):
        return text.strip().strip(param).strip()
      
