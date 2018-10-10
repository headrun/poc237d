start_urls_list = ['https://www.interpol.int/notice/search/wanted']
fields_list = ["url", "Family_name", "Criminal_Name", "sex", "Date_of_birth", "Place_of_birth", "Language_spoken", "Nationality", "Charges", "Regions_where_wanted"]
headers_list = {
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Origin': 'https://www.interpol.int',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'https://www.interpol.int/extension/design_sqli/design/design_sqli/stylesheets/master.css',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
