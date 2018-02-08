# -*- coding: utf-8 -*-
import csv
import os
import datetime
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class Karnataka(object):

    """Gathering Karnataka judiciary csv files"""

    def __init__(self):
        self.main_path = os.path.dirname(os.getcwd())
        self.csv_path = os.path.join(
            self.main_path, 'spiders', datetime.datetime.now().strftime('%Y/%m/%d'))

    def get_compressed_file(self):
        """ from here returning compressed tar file """
        os.chdir(self.csv_path)
        gz_file = 'KPMGKAPOC_%s.tar.gz' % str(
            datetime.datetime.now().date().strftime('%d%m%Y'))
        gz_cmd = 'tar -czf %s *csv' % gz_file
        os.system(gz_cmd)
        return gz_file

    def move_to_processed(self):
        """Moving to processed"""
        os.chdir(self.csv_path)
        processed_path = '%s/processed' % self.csv_path
        if not os.path.isdir(processed_path):
            os.makedirs(processed_path)
        mv_cmd = 'mv *csv *gz processed'
        os.system(mv_cmd)
        print mv_cmd

    def main(self):
        """sending mail starts from here"""
        try:
            recievers_list = ['delivery@headrun.com', 'sathwick@headrun.com']
            sender, receivers = 'headrunkpmgproject@gmail.com', ','.join(
                recievers_list)
            ccing = ['aravind@headrun.com',
                     'raja@headrun.com', 'jaideep@headrun.com']
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'KPMG POC: Karnataka Judiciary Data on %s' % (
                str(datetime.datetime.now().date()))
            mas = '<h3>Hi Team,</h3>'
            mas += '<p>Please find the karnataka judiciary data in the below attachment</p>'
            mas += '<table  border="1" cellpadding="0" cellspacing="0" >'
            mas += '<tr><th>Keyword</th><th>File name</th><th> Number of records</th>'
            gb_file = self.get_compressed_file()
            for csvfile in os.listdir(self.csv_path):
                if csvfile.endswith('.csv'):
                    no_of_records = len(list(csv.reader(open(csvfile, "r+"))))
                    mas += '<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (
                        csvfile.split('_')[0].replace('-', ' '), csvfile, no_of_records)
            mas += '</table>\n\n\n'
            mas += '<br>Note : No of records with 0\
         indicates no results for that particular keyword.'
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(gb_file, "rb").read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition', 'attachment', filename=gb_file)
            msg.attach(part)
            msg['From'] = sender
            msg['To'] = receivers
            msg['Cc'] = ",".join(ccing)
            tem = MIMEText(''.join(mas), 'html')
            msg.attach(tem)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, 'Hkpmgprj')
            total_mail = (recievers_list) + ccing
            server.sendmail(sender, (total_mail), msg.as_string())
            server.quit()
            print 'success'
            self.move_to_processed()
        except Exception as error:
            logging.exception(error)

if __name__ == '__main__':
    Karnataka().main()
