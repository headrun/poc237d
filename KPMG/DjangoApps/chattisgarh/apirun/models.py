from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CaseDetails(models.Model):
    keyword = models.CharField(max_length=128)
    year = models.CharField(max_length=128)
    case_number = models.CharField(max_length=128)
    petitioner = models.CharField(max_length=128)
    petitioner_advocate = models.TextField()
    respondent = models.CharField(max_length=128)
    respondent_advocate = models.TextField()
    case_status = models.CharField(max_length=128)
    decision_date = models.DateTimeField()
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'case_details'
        unique_together = (('case_number', 'petitioner', 'respondent'),)
    def __str__(self):
	return self.case_number
