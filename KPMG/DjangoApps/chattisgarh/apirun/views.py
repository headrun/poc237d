from django.shortcuts import render
from django.http import HttpResponse
from .models import CaseDetails
import simplejson
from datetime import datetime
import os

# Create your views here.


def index(request):
	pet_name = request.GET.get('keyword', None)
	year = request.GET.get('year', None)

	if not pet_name: return HttpResponse(simplejson.dumps({"response":"Arguments are missing"}))

	if not year: year= datetime.now().year
	
	cmd = "cd /home/headrun/akram/repository/poc237/chhattisgarhpoc/chhattisgarhpoc/spiders/; scrapy runspider hc_chattisghar_browse.py -a word='{0}' -a year='{1}'".format(pet_name, year)
	print cmd
	os.system(cmd)
	obj = CaseDetails.objects.filter(keyword=pet_name).filter(year=year)
	record = {'data':[], 'keyword':pet_name, 'year':year}
	for e in obj.iterator():
		if e.decision_date:decision_dt = e.decision_date.isoformat()
		else: decision_dt = None
		c = {'respondent':e.respondent, 'petitioner_advocate':e.petitioner_advocate,
			'petitioner':e.petitioner, 'case_status':e.case_status, 'respondent_advocate':e.respondent_advocate,
			'case_number':e.case_number, 'decision_date':decision_dt}
		record['data'].append(c)
	
	return HttpResponse(simplejson.dumps(record), content_type="application/json")
