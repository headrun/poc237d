import scrapy
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
import re
import json
import csv
import datetime

class Linkedin_companies(scrapy.Spider):
    name = 'linkedin_companies'
    allowed_domains = ["linkedin.com"]
    start_urls = ('https://www.linkedin.com/uas/login?goback=&trk=hb_signin',)
    def __init__(self, *args, **kwargs):
	self.excel_file_name = 'linkedinjobs_data_%s.csv'%str(datetime.datetime.now().date())
	oupf = open(self.excel_file_name, 'ab+')
	self.todays_excel_file  = csv.writer(oupf)
	self.header_params = ['company_id', 'jobview_url', 'Position(Company)']
	self.todays_excel_file.writerow(self.header_params)
	

    def parse(self,response):
	sel = Selector(response)
        command_prxy = cvs = response.meta.get('proxy','')\
        .replace('http://','').replace(':3279','')\
        .replace('https://','')
        logincsrf = ''.join(sel.xpath('//input[@name="loginCsrfParam"]/@value').extract())
        csrf_token = ''.join(sel.xpath('//input[@id="csrfToken-login"]/@value').extract())
        source_alias = ''.join(sel.xpath('//input[@name="sourceAlias"]/@value').extract())
        return [FormRequest.from_response(response, formname = 'login_form',\
                formdata=
{'session_key':'ramyalatha3004@gmail.com','session_password':'01491a0237','isJsEnabled':'','source_app':'','tryCount':'','clickedSuggestion':'','signin':'Sign In','session_redirect':'','trk':'hb_signin','loginCsrfParam':logincsrf,'fromEmail':'','csrfToken':csrf_token,'sourceAlias':source_alias},callback=self.parse_next, meta = {"csrf_token":csrf_token})]


    def parse_next(self,response):
	cooki_list = response.request.headers.get('Cookie', [])
	li_at_cookie = ''.join(re.findall('li_at=(.*?); ', cooki_list))
        headers = {
                'cookie': 'li_at=%s;JSESSIONID="%s"' % (li_at_cookie, response.meta['csrf_token']),
                'x-requested-with': 'XMLHttpRequest',
                'csrf-token': response.meta['csrf_token'],
                'authority': 'www.linkedin.com',
                'referer': 'https://www.linkedin.com/',
                }
	api_key = 'decoration=%28hitInfo%28com.linkedin.voyager.search.SearchJobJserp%28descriptionSnippet%2CjobPosting~%28entityUrn%2CsavingInfo%2Ctitle%2CformattedLocation%2CapplyingInfo%2Cnew%2CjobState%2CsourceDomain%2CapplyMethod%28com.linkedin.voyager.jobs.OffsiteApply%2Ccom.linkedin.voyager.jobs.SimpleOnsiteApply%2Ccom.linkedin.voyager.jobs.ComplexOnsiteApply%29%2ClistedAt%2CexpireAt%2CclosedAt%2CcompanyDetails%28com.linkedin.voyager.jobs.JobPostingCompany%28company~%28entityUrn%2Cname%2Clogo%2CbackgroundCoverImage%29%29%2Ccom.linkedin.voyager.jobs.JobPostingCompanyName%29%2CeligibleForReferrals%2C~relevanceReason%28entityUrn%2CjobPosting%2Cdetails%28com.linkedin.voyager.jobs.shared.InNetworkRelevanceReasonDetails%28totalNumberOfConnections%2CtopConnections*~%28profilePicture%2CfirstName%2ClastName%2CentityUrn%29%29%2Ccom.linkedin.voyager.jobs.shared.CompanyRecruitRelevanceReasonDetails%28totalNumberOfPastCoworkers%2CcurrentCompany~%28entityUrn%2Cname%2Clogo%2CbackgroundCoverImage%29%29%2Ccom.linkedin.voyager.jobs.shared.SchoolRecruitRelevanceReasonDetails%28totalNumberOfAlumni%2CmostRecentSchool~%28entityUrn%2Cname%2Clogo%29%29%2Ccom.linkedin.voyager.jobs.shared.HiddenGemRelevanceReasonDetails%29%29%2C~jobSeekerQuality%28entityUrn%2CqualityType%2CqualityToken%2CmessagingStatus%29%29%29%2Ccom.linkedin.voyager.search.FacetSuggestion%2Ccom.linkedin.voyager.search.SearchCompany%2Ccom.linkedin.voyager.search.SearchJob%2Ccom.linkedin.voyager.search.SearchProfile%2Ccom.linkedin.voyager.search.SearchSchool%2Ccom.linkedin.voyager.search.SecondaryResultContainer%29%2CtrackingId%29&count=25'
	api_url_inner = "https://www.linkedin.com/voyager/api/search/hits?"
	api_url_withkeyword = "&keywords=Python%20Scraping&location=Bengaluru%2C%20Karnataka%2C%20India&origin=JOB_SEARCH_RESULTS_PAGE&q=jserpAll&query=search&refresh=true"
	api_url = "%s%s%s"% (api_url_inner, api_key, api_url_withkeyword)
	api_url ="%s%s%s%s" % (api_url_inner, api_key,self.location,self.keyword)
        yield Request(api_url, callback = self.parse_again, headers = headers)

    def parse_again(self, response):
	import pdb;pdb.set_trace()
	json_tmp = json.loads(response.body)
	json_elements = json_tmp.get('elements', [])
	headers = {
		'authority': 'www.linkedin.com',        
		'referer': 'https://www.linkedin.com/',              
		}
	for element in json_elements:
		compnay_id = ''.join(element.get('hitInfo',{}).get('com.linkedin.voyager.search.SearchJobJserp',{}).get('jobPosting',''))
		compnay_full_id = compnay_id.split('jobPosting:')[-1]
		job_view_url = ''.join("https://www.linkedin.com/jobs/view/%s/" % (compnay_full_id))
		company_title = ''.join(element.get('hitInfo',{}).get('com.linkedin.voyager.search.SearchJobJserp',{}).get('jobPostingResolutionResult', {}).get('title',''))
		values = [compnay_full_id, job_view_url, company_title]
		self.todays_excel_file.writerow(values)

"""

		
		f=file("date","ab+").write("%s\n" %file)
		#values = [xcode(compnay_id),xcode(job_view_url),xcode(company_title)]
		#self.fp.write('%s\n' %values)
		#self.fp.flush()
		f = open("file","a")
		f.write(compnay_id)
		f.write("\n")
		f.write(compnay_full_id)
		f.write("\n")
		f.write(job_view_url)
		f.write("\n")
		f.write(company_title)
		f.write("\n")
		f.close()
"""
