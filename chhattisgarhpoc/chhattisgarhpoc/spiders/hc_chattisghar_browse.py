import re
import csv
import datetime
from scrapy.http import Request, FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector


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
        self.path = kwargs.get('path', '')
        self.excel_file_name = self.path + '/%s_%s_%s_hc_chhattisgarh.csv'%(self.word.replace(' ', '-'), self.year, str(datetime.datetime.now().date()))
        self.oupf = open(self.excel_file_name, 'w+')
        self.todays_excel_file = csv.writer(self.oupf) 
        court_headers = ['Case number', 'Petitioner', 'Petitioner Advocate', 'Respondent', 'Respondent Advocate', 'Case status', 'Decision Date']
        self.todays_excel_file.writerow(court_headers)


    def parse(self, response):
	sel = Selector(response)
        headers = response.headers
        sid = sel.xpath('//input[@name="__csrf_magic"]/@value').extract()
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
        sel = Selector(text=normalize(response.body))  
       	pet_details = '\n'.join(sel.xpath('//span[@class="Petitioner_Advocate_table"]/text()').extract())
	resp_details = '\n'.join(sel.xpath('//span[@class="Respondent_Advocate_table"]/text()').extract())
        case_num = ''.join(sel.xpath('//label[contains(text(), "Registration Number")]/../../label/text()').extract()).strip(':').strip().split('/')[0]

        pet_adv, pet_add = '', ''
        resp_adv, resp_add = '', ''
        peti, respi = '', ''
        status = ''
        if pet_details:
            peti = pet_details.split('\n')[0].strip().split('1)')[-1].strip().strip(',').strip()
            pet_adv = ''.join(re.findall('Advocate(.*)', pet_details)).strip().strip('-').strip().replace('Advocate', '').strip('-').strip()
            pet_add = ''.join(re.findall('Address(.*)', pet_details)).strip().strip('-').strip()

        if resp_details:
            respi = resp_details.split('\n')[0].strip().split('1)')[-1].strip().strip(',').strip()
            resp_adv = ''.join(re.findall('Advocate(.*)', resp_details)).strip().strip('-').strip().replace('Advocate', '').strip('-').strip()
            resp_add = ''.join(re.findall('Address(.*)', resp_details)).strip().strip('-').strip()

        status = ''.join(sel.xpath('//strong[contains(text(), "Case Status ")]/following-sibling::strong/text()').extract()).strip(':')     

        if not status:
            status = ''.join(sel.xpath('//strong[contains(text(), "Stage of Case")]/following-sibling::strong/text()').extract()).strip(':') 

        decision_date = ''.join(sel.xpath('//strong[contains(text(), "Decision Date")]/following-sibling::strong/text()').extract()).strip(':')
        court_values = [case_num, peti.strip(), pet_adv.strip(',').strip(), respi.strip(), resp_adv.strip().strip(',').strip(), status.strip(), decision_date]
        court_values = [e.replace(u'\xa0', ' ').replace(',,', ',').strip() for e in court_values]
        
        self.todays_excel_file.writerow(court_values)
         
