KPMG POC Scrappers:
=============================

### Installation setup:

```
sudo pip install scrapy==1.4.0
```

## Steps:

1/ Navigate to spiders path

```
cd kpmgkapoc/spiders
```

2/ Run the scraper 

```
-a bench="Bengaluru Bench/ Dharwad Bench/ Kalaburagi Bench" default is Bengaluru Branch
-a who="Petitioner/Responder/Don't know" default is Don't Know
-a dist="" - default is Don't Know
-a ctype='' - default is Don't Know
```

Below are mandatory
```
*-a resp="<Name of respondent or petitioner>"
*-a from="dd/mm/yyyy" - Filing from date
*-a to="dd/mm/yyyy" - Filing to date
```


```
scrapy crawl karnatakajudiciary_browse -a resp='Savitha' -a from='10/02/2017' -a to='02/01/2018' -o files.csv -t csv
```

(or)

3/ Write a list of keywords into input_file.txt and then run the python script. 

```
python karnatakajudiciary_wrapper.py
```

This will generate csv files in the  path ./year/month/day/* with name <keyword_dd_mm_yyyy.csv>

4/ To send emails to recipients

might have to change the recipients.

```
python karnatakajudiciary_mail.py
```
