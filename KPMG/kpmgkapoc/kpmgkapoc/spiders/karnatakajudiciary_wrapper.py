# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta

class Kpmgwrapper(object):
    """ Wrapper file for scrapper """

    def main(self):
        file_name = 'input_file.txt'
        back_dated_by = 365
        back_date = (datetime.now() - timedelta(days=back_dated_by)).date().strftime("%d/%m/%Y")
        todays_date = datetime.now().date().strftime("%d/%m/%Y")
        mydir = os.path.join(os.getcwd(), datetime.now().strftime('%Y/%m/%d'))
        if not os.path.isdir(mydir):
            os.makedirs(mydir)
        if os.path.isfile(file_name):
            with open(file_name, 'r') as f: rows = f.readlines()
            for i in ['Dharwad Bench', 'Bengaluru Bench', 'Kalaburagi Bench']:
                for row in rows:
                    row = row.replace('\r\n','').strip()
                    file_locations = os.path.join(mydir, row.replace(' ', '-'))
                    cmd = "scrapy crawl karnatakajudiciary_browse -a resp='%s' -a bench='%s' -a from='%s' -a to='%s' -o %s_%s_%s.csv -t csv" % (row, i, back_date, todays_date, file_locations, i.replace(' Bench', '').lower(), todays_date.replace('/', '_'))
                    os.system(cmd)
        else:
            print 'Specify input file location properly'


if __name__ == '__main__':
    Kpmgwrapper().main()
