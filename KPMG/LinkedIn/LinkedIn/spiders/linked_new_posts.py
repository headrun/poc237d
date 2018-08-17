import scrapy
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
import re
import json
import csv
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class Linkedin_companies(scrapy.Spider):
    name = 'plinkedin_posts'
    allowed_domains = ["linkedin.com"]
    start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)

    def __init__(self, *args, **kwargs):
        self.excel_file_name = 'linkedinfull_data_%s.csv' % str(
            datetime.datetime.now().date())
        oupf = open(self.excel_file_name, 'ab+')
        self.todays_excel_file = csv.writer(oupf)
        self.header_params = ['First Name', 'Last Name', 'Occupation', 'Information','Likes','Comments']
        self.todays_excel_file.writerow(self.header_params)

    def parse(self, response):
	sel = Selector(response)
	logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
	csrf_token = ''.join(sel.xpath('//input[@id="csrfToken-login"]/@value').extract())
	source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
	data = [
	  ('isJsEnabled', 'true'),
	  ('source_app', ''),
	  ('tryCount', ''),
	  ('clickedSuggestion', 'false'),
	  ('session_key', 'ramyalatha3004@gmail.com'),
	  ('session_password', '01491a0237'),
	  ('signin', 'Sign In'),
	  ('session_redirect', ''),
	  ('trk', 'hb_signin'),
	  ('loginCsrfParam', logincsrf),
	  ('fromEmail', ''),
	  ('csrfToken', csrf_token),
	  ('sourceAlias', source_alias),
	  ('client_v', '1.0.1'),
	]
	headers = {
	    'cookie': response.headers.getlist('Set-Cookie'),
	    'origin': 'https://www.linkedin.com',
	    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
	    'x-requested-with': 'XMLHttpRequest',
	    'x-isajaxform': '1',
	    'accept-encoding': 'gzip, deflate, br',
	    'pragma': 'no-cache',
	    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
	    'content-type': 'application/x-www-form-urlencoded',
	    'accept': '*/*',
	    'cache-control': 'no-cache',
	    'authority': 'www.linkedin.com',
	    'referer': 'https://www.linkedin.com/',
	}
	yield FormRequest('https://www.linkedin.com/uas/login-submit', callback=self.parse_next, formdata=data, headers = headers, meta = {"csrf_token":csrf_token})



    def parse_next(self, response):
        cooki_list = response.request.headers.get('Cookie', [])
	
        li_at_cookie = ''.join(re.findall('li_at=(.*?); ', cooki_list))
        headers = {
            'cookie': 'li_at=%s;JSESSIONID="%s"' % (li_at_cookie, response.meta['csrf_token']),
                'x-restli-protocol-version': '2.0.0',
                'x-requested-with': 'XMLHttpRequest',
                'csrf-token': response.meta['csrf_token'],
                'authority': 'www.linkedin.com',
                'referer': 'https://www.linkedin.com/search/results/index/?keywords=kpmg&origin=GLOBAL_SEARCH_HEADER',
        }
	api_url = "https://www.linkedin.com/voyager/api/search/cluster?count=6&guides=List(v-%3ECONTENT)&keywords=kpmg&origin=SWITCH_SEARCH_VERTICAL&q=guided&start=0"
        yield Request(api_url, callback=self.parse_last, headers=headers, meta = {'api_first_url':api_url})
	api01 = "https://www.linkedin.com/voyager/api/search/hits?count=6&guides=List(v-%3ECONTENT)&keywords=kpmg&origin=SWITCH_SEARCH_VERTICAL&q=guided&start=6"
	api_nav = "https://www.linkedin.com/voyager/api/search/hits?count=6&guides=List(v-%3ECONTENT)&keywords=kpmg&origin=SWITCH_SEARCH_VERTICAL&q=guided"
	yield Request(api01, callback=self.parse_navigation, headers=headers, meta = {'api_next':api01, 'api_nav':api_nav, 'headers':headers})
	

    def parse_last(self, response):
	json_tmp = json.loads(response.body)
        json_elements = json_tmp.get('elements',[])
        headers = {
        'authority': 'www.linkedin.com',
        'referer': 'https://www.linkedin.com/',
        }
        inner_elements = []
        for element in json_elements:
                inner_elements = element.get('elements')
                for each in inner_elements:
                        profile = each.get('hitInfo', {}).get('com.linkedin.voyager.feed.Update',{}).get('value',{}).get('com.linkedin.voyager.feed.ShareUpdate',{}).get('actor',{}).get('com.linkedin.voyager.feed.MemberActor',{}).get('miniProfile',{})
                        if profile:
                                first_name = profile.get('firstName','')
                                last_name = profile.get('lastName','')
                                occupation = profile.get('occupation','')
                        	content = each.get('hitInfo', {}).get('com.linkedin.voyager.feed.Update',{}).get('value',{}).get('com.linkedin.voyager.feed.ShareUpdate',{}).get('content',{}).get('com.linkedin.voyager.feed.ShareText',{}).get('text',{}).get('values','')
                                for info in content:
                                        information = info.get('value','')
					likes = each.get('hitInfo',{}).get('com.linkedin.voyager.feed.Update',{}).get('socialDetail',{}).get('totalSocialActivityCounts',{}).get('numLikes','')
					comments = each.get('hitInfo', {}).get('com.linkedin.voyager.feed.Update',{}).get('socialDetail',{}).get('totalSocialActivityCounts',{}).get('numComments','')
					values = [first_name,last_name,occupation,information,likes,comments]
					self.todays_excel_file.writerow(values)
                        else:
                                profile = each.get('hitInfo',{}).get('com.linkedin.voyager.feed.Update',{}).get('value',{}).get('com.linkedin.voyager.feed.ArticleUpdate',{}).get('content',{}).get('com.linkedin.voyager.feed.ShareArticle',{}).get('article',{}).get('article',{}).get('title','')
                        	likes = each.get('hitInfo',{}).get('com.linkedin.voyager.feed.Update',{}).get('socialDetail',{}).get('totalSocialActivityCounts',{}).get('numLikes','')
                        	comments = each.get('hitInfo', {}).get('com.linkedin.voyager.feed.Update',{}).get('socialDetail',{}).get('totalSocialActivityCounts',{}).get('numComments','')	
				values = [profile,'','','',likes,comments]
				self.todays_excel_file.writerow(values)
    def parse_navigation(self, response):
	data = json.loads(response.body)
	json_info = data.get('elements',[])
	#inner_elements = []
        #for element in json_info:
                #inner_elements = element.get('elements')
	api_next = response.meta.get('api_next',{})
	api_nav = response.meta.get('api_nav',{})
	if api_next:
		url_paging  = data.get('paging',[])
		if url_paging:
		    count_data = url_paging.get('count','')
		    start_data = url_paging.get('start','')
		    total_data = url_paging.get('total','')
		    if total_data > count_data+start_data:
			cons_part = api_nav + "&start=%s"%(start_data+count_data)
			retrun_url = cons_part
			#if inner_elements:
			yield Request(retrun_url, callback=self.parse_last)



