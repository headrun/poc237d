## Punjab and Haryana HC

Steps to be followed to run the scraper.


Navigate to spiders path

    cd punjabharyanahc/spiders

Run the scraper by sending the below arguments.
      
	- Name[keyword]
	- Registration From Date(Optional)[from_date]       
	- Registration To Date(Optional)[to_date]
	- Path to store the csv files(Optional)[path]
	  
#### `Example:`

	scrapy runspider punjab_highcourt.py -a keyword='<keyword>' -a from_date='<from_date>' -a to_date='<to_date>' -a path='<path>'

(or)

Write list of names from and to date seperated with Vertical bar Pipe(|) in inputs.txt and then run the python script as below.

input file samples:

	lal mishra||
	gaurav|10/04/2017|10/04/2018
	lakshmi|01/12/2017|09/05/2018


Note:The from, to dates should be in DD/MM/YYYY format only

	python punjabhc_wrapper.py

This will generate csv files in the following path csv_files/YYYY-MM-DD/<keyword>_<from_date>_<to_date>_hc_punjab-haryana_YYYY-MM-DD.csv
