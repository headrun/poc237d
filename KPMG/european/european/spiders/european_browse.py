# -*- coding: utf-8 -*-
import csv, re
import datetime
from scrapy.http     import  Request, FormRequest
from scrapy.spider   import BaseSpider
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
import requests
class EUROPEAN(BaseSpider):
    name = 'european_browse'
    start_urls = ['http://curia.europa.eu/juris/recherche.jsf?language=en']

    def __init__(self, prtynme='', **kwargs):
        super(EUROPEAN, self).__init__(**kwargs)
        self.prtynme = prtynme
        self.headers = ['Case Number', 'Title', 'Case Status', 'Description', 'Date of Hearing',
                        'Date of Delivery', 'Advocate', 'Result']
        oupf1 = open('curia-%s-%s.csv'  % (self.prtynme, str(datetime.date.today())), 'wb+')
        self.csv_file = csv.writer(oupf1)
        self.csv_file.writerow(self.headers)
        self.headings = ['Case Number', 'Doc', 'Date', 'Parties', 'petitioner','appellant', 'respondent', 'Subject-Matter']
        oupf2 = open('curia-%s-documents-%s.csv' %(self.prtynme, str(datetime.date.today())), 'wb+')
        self.document_file = csv.writer(oupf2)
        self.document_file.writerow(self.headings)
        self.terminal_crawl = True
        self.headers = {'Origin': 'http://curia.europa.eu',
                        'Connection': 'keep-alive',
                        'Accept-Language': 'en-US,en;q=0.9,fil;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Pragma': 'no-cache',
                        'Cache-Control': 'no-cache',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Accept': '*/*',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

    def parse(self, response):
        dat1 = response.headers.getlist('Set-cookie')
        cook = {}
        for i in dat1:
            davn = i.split(';')[0]
            if davn:
                try:
                    key, val = davn.split('=', 1)
                except:
                    continue
                cook.update({key.strip():val.strip()})
        cookies = {'JSESSIONID': cook.get('JSESSIONID', '')}
        j_id = 1
        yield FormRequest('http://curia.europa.eu/juris/liste.jsf?pro=&nat=or&oqp=&dates=&lg=&language=en&jur=C%2CT%2CF&cit=none%252CC%252CCJ%252CR%252C2008E%252C%252C%252C%252C%252C%252C%252C%252C%252C%252Ctrue%252Cfalse%252Cfalse&td=%3BALL&pcs=Oor&avg=&page=1&mat=or&parties='+self.prtynme+'&jge=&for=&cid=137525', headers=self.headers, cookies=cookies, callback=self.parse_next, meta={'j_id':j_id})
 

    def parse_next(self, response):
        sel = Selector(response)
        j_id = response.meta['j_id']
        dat1 = response.headers.getlist('Set-cookie')
        cook = {}
        for i in dat1:
            davn = i.split(';')[0]
            if davn:
                try: key, val = davn.split('=', 1)
                except: continue
                cook.update({key.strip():val.strip()})
        cookies = {'JSESSIONID': cook.get('JSESSIONID', '')}

        nodes = sel.xpath("//div[@class='affaire']")
        for node in nodes:
            title = ''.join(node.xpath(".//span[@class='affaire_title']//text()").extract()).strip()
            title  = title.replace('\n ', '')
            case_no = '-'.join(title.split('-')[0:2])
            case_status = ''.join(node.xpath('.//tr//td//span[@class="affaire_status"]//text()').extract()).strip()
            description = ''.join(node.xpath(".//div[@class='decision_title']//p//text()").extract()).encode('utf-8').strip()
            if j_id == 1:
                link = ''.join(node.xpath(".//span[@class='decision_links']//a//@href").extract())
            else:
                link = ''.join(node.xpath('.//div[@class="decision"]/table/tr//td[@class="decision"]/span[@class="decision_links"]/a/@href')[1].extract())
            meta = {'Case_no': case_no, 'description': description, 'case_status': case_status, 'j_id':j_id}
            yield Request(link, callback=self.parse_md1, meta=meta)

        if self.terminal_crawl:
            page_details = {}
            self.terminal_crawl = False
            pg_nodes = sel.xpath('//div[@class="pagination"]/a/span')
            for pg_node in pg_nodes:
                pg_num = ''.join(pg_node.xpath('./text()').extract())
                pg_id = ''.join(pg_node.xpath('.//../@id').extract()).split(':')[-1]
                if pg_num == '1':
                    continue
                page_details.update({pg_num: pg_id})

                for key, val in page_details.iteritems():
                    j_id = j_id + 1
                    mainform = ''.join(sel.xpath('//div[@id="header_lang"]/select/@name').extract()).split(':')[-1]
                    data = [
                        ('AJAXREQUEST', '_viewRoot'),
                        ('mainForm', 'mainForm'),
                        ('mainForm:%s' % mainform, 'en'),
                        ('lienImage', '/juris'),
                        ('javax.faces.ViewState', 'j_id%s' % str(j_id)),
                        ('mainForm:%s' % val, 'mainForm:%s' % val),
                        ('page', key),
                        ('', ''),
                        ]
                    url = 'http://curia.europa.eu/juris/liste.jsf'
                    meta = {'cookies': cookies, 'j_id':j_id}
                    yield FormRequest(url, callback=self.parse_ajax, headers=self.headers, cookies=cookies, formdata=data, meta=meta)

    def parse_ajax(self, response):
        cookies = response.meta['cookies']
        next_url = response.body.split('content=')[-1].replace(' /></head></html>', '').strip('"')
        if 'http' not in next_url:
            next_url = 'http://curia.europa.eu' + next_url
        yield Request(next_url, callback = self.parse_next, headers=self.headers, cookies=cookies, meta={'j_id':response.meta['j_id']})

    def parse_md1(self, response):
        sel = Selector(response)
        delivery = ''.join(sel.xpath('//div[@class="detail_zone_content"]//h3[contains(text(), "delivery")]/following-sibling::p[1]//text()').extract()).strip()
        hearing = ''.join(sel.xpath('//div[@class="detail_zone_content"]//h3[contains(text(), "hearing")]/following-sibling::p[1]//text()').extract()).strip()
        parties = ''.join(sel.xpath('//div[@class="detail_zone_content"]//h3[contains(text(), "parties")]/following-sibling::p[1]//text()').extract()).encode('utf-8').strip()
        advocate = ''.join(sel.xpath('//div[@class="detail_zone_content"]//h3[contains(text(), "Advocate")]/following-sibling::p//text()').extract()).encode('utf-8').strip()
        result = ''.join(sel.xpath('//div[@class="detail_zone_content"]//h3[contains(text(), "result")]//following-sibling::ul[1]//li[contains(@id, "mainForm:j_id")]//text()').extract()).strip().encode('utf-8').strip()
        case = response.meta.get('Case_no', '')
        description = response.meta.get('description', '')
        case_st = response.meta.get('case_status','')
        values = [case, parties, case_st, description, hearing, delivery, advocate, result]
        self.csv_file.writerow(values)

        yield Request('http://curia.europa.eu/juris/documents.jsf?pro=&nat=or&oqp=&dates=&lg=&language=en&jur=C%2CT%2CF&cit=none%252CC%252C    CJ%252CR%252C2008E%252C%252C%252C%252C%252C%252C%252C%252C%252C%252Ctrue%252Cfalse%252Cfalse&td=%3BALL&pcs=Oor&avg=&page=1&mat=or&parties='    +self.prtynme+'&jge=&for=&cid=137525', callback=self.parse_md2)

    def parse_md2(self, response):
        sel = Selector(response)
        nodes = sel.xpath('//table[@class="detail_table_documents"]//tr[@class="table_document_ligne"]')
        for node in nodes:
            caseno = ''.join(node.xpath('.//td[@class="table_cell_aff"]//text()').extract()).strip()
            if 'OpenWin' in caseno:
                caseno = ''.join(node.xpath('.//td[@class="table_cell_aff"]//text()').extract()).strip().split('\n')[0]
            doc = ''.join(node.xpath('.//td[@class="table_cell_doc"]//text()').extract()).strip()
            date = ''.join(node.xpath('.//td[@class="table_cell_date"]//text()').extract()).strip()
            nparties = ''.join(node.xpath('.//td[@class="table_cell_nom_usuel"]//text()').extract()).strip().encode('ascii', 'ignore')
            petitioner, respondent, appellant = '', '', ''
            if ' v ' in nparties:
                petitioner = nparties.split(' v ')[0]
                respondent = nparties.split(' v ')[1]

            else:
                petitioner = nparties
                respondent = ''

                if '' in respondent:
                    links = ''.join(node.xpath('.//td/div[@id="docHtml"]/a/@href').extract())
                    if links:
                        res = requests.get(links)
                        sel = Selector(text = res.text)
                        nodes = sel.xpath('//div[@id="document_content"]') 
                        inside_page = nodes.xpath('//p[b[contains(text(), "Parties to the main proceedings")]]/following-sibling::p[i]/text()').extract()
                        if inside_page:
                            petitioner = ''
                            appellant = inside_page[0]
                            respondent = inside_page[1]
                            values = [petitioner, appellant, respondent]
                            if values:
                                petitioner= values[0].encode('ascii', 'ignore') 
                                appellant = values[1].encode('ascii', 'ignore')
                                respondent = values[2].encode('ascii', 'ignore')
                            else:
                                continue
                        if '' in inside_page:
                            petitioner = nparties
                            respondent = ''
            subjectmatter = ''.join(node.xpath('.//td[@class="table_cell_links_curia"]//text()').extract()).strip()
            values = [caseno, doc, date, nparties, petitioner, appellant, respondent, subjectmatter]
            self.document_file.writerow(values)

        nxt_pg = response.xpath('//a[img[@alt="Show next document"]]/@href').extract()
        nxt = ''.join(nxt_pg)
        
        if nxt:
            yield Request(nxt, callback=self.parse_md2)
        
            
