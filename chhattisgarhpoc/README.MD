Running the crawler for the input.

1. Navigate to spiders path

    cd chhattisgarhpoc/spiders

2. Run the scraper by sending the below mandatory arguments.
      * Petitioner Name
      * Year           
      * Path            - The directory to store the csv file.

Example:
scrapy crawl chhattisghar_browse -a word='gaurav' -a year='2017' -a path='csv_files'


(or)

1. Write a list of petitioner name and year seperated with Vertical bar Pipe(|) into input_file.txt and then run the python script.

input file samples:

lal mishra|2018


gaurav|2017

python hc_chattisghar_wrapper.py

This will generate csv files in the following path csv_files/YYYY-MM-DD/<word>_<year>_YYYY-MM-DD_hc_chhattisgarh.csv
