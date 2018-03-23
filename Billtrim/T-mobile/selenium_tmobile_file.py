from selenium import webdriver
from base64 import b64encode
import time
import datetime
import csv
import os
from lxml import etree

def get_proxy_driver(PROXY_HOST,PROXY_PORT):
        fp = webdriver.FirefoxProfile()
        print PROXY_PORT
        print PROXY_HOST
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http",PROXY_HOST)
        fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
        fp.set_preference("network.proxy.https",PROXY_HOST)
        fp.set_preference("network.proxy.https_port",int(PROXY_PORT))
        fp.set_preference("network.proxy.ssl",PROXY_HOST)
        fp.set_preference("network.proxy.ssl_port",int(PROXY_PORT))  
        fp.set_preference("network.proxy.ftp",PROXY_HOST)
        fp.set_preference("network.proxy.ftp_port",int(PROXY_PORT))   
        fp.set_preference("network.proxy.socks",PROXY_HOST)
        fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))   
        fp.update_preferences()
        return webdriver.Firefox(firefox_profile=fp)


class Tmobile():
	def main(self):
		headers = ['Due Amount', 'Due date', 'Logged in Usernme', 'Autopay', 'Next payment schedule', 'Billing Name', 'Billing Msisdn', 'Billing plan type', 'Billing Plan name', 'Billing past due', 'Billing Talk minutes', 'Billing Txt msg', 'Billing Data speed', 'Billing Bing on Desc', 'Billing device image']
		filename = "Tmobile_POC.csv"
                csv_file = self.is_path_file_name(filename)
                csv_file.writerow(headers)
		driver = get_proxy_driver('47.206.51.67', '8080')
		driver.get('https://account.t-mobile.com/oauth2/v1/auth?redirect_uri=https:%2F%2Fmy.t-mobile.com&scope=TMO_ID_profile%20associated_lines%20billing_information%20associated_billing_accounts%20extended_lines%20token&client_id=A-3amGd14-iz0&access_type=ONLINE&response_type=code&approval_prompt=auto&state=false&state=false')
		time.sleep(1)
		driver.find_element_by_xpath('//input[@id="username"]').clear()
		driver.find_element_by_xpath('//input[@id="username"]').send_keys("315-731-7750")
		driver.find_element_by_xpath('//input[@id="password"]').clear()
		driver.find_element_by_xpath('//input[@id="password"]').send_keys("M@bilePINK77$$")
		driver.find_element_by_xpath('//input[@value="LOG IN"]').click()
		time.sleep(25)
		driver.find_element_by_xpath('//div[@class="accordion-heading2"]').click()
		driver.save_screenshot('screenshot_on_%s.png' % str(datetime.datetime.now().date()))
		time.sleep(5)
		html_source = driver.page_source
		sel =  etree.HTML(html_source)
		due_amount = ''.join(sel.xpath('//div[@id="di_balDueAmount"]/text()'))
		due_date = ''.join(sel.xpath('//div[@id="di_dueDate"]/text()'))
		logged_usernam = ''.join(sel.xpath('//span[@id="loggedInUserName"]/text()'))
		autopay = ''.join(sel.xpath('//div[@id="easyPayWithoutDiscount"]//a/span/text()'))
		next_payment_schedule = ''.join(sel.xpath('//div[@id="easyPayMessageON"]//b/text()'))
		nodes = sel.xpath('//div[@class="profileDummy"]/div')
		for nod in nodes:
			name_ = ''.join(nod.xpath('.//span[@class="firstName"]/text()'))
			msisdn_ = ''.join(nod.xpath('.//span[@class="msisdn ui_body"]/text()'))
			plan_type_ = ''.join(nod.xpath('.//div[@class="ui_caps_headline mt35 "]/text()'))
			plan_name_ = ''.join(nod.xpath('.//span[@class="planName"]/text()'))
			billing_pastdue = ' '.join(nod.xpath('.//div[@class="ui_billingpastdue"]//span//text()'))
			billing_talk_minutes = ' '.join(nod.xpath('.//div[@class="pull-left mr30 talk-minutes dataTalkMinutesExist hide"]/div[not(contains(@class, "headline"))]//text()')).replace('  ', ' ')
			billing_txt_msg = ' '.join(nod.xpath('.//div[@class="pull-left mr25 text-msgs dataTextMsgsExist hide"]/div[not(contains(@class, "headline"))]//text()')).replace('  ', ' ')
			billing_data_speed = ' '.join(nod.xpath('.//div[@class="pull-left mr20 mr35 data-speed dataSpeedExist"]/div[not(contains(@class, "headline"))]//text()')).replace('  ', ' ')
			bing_on_desc = ' '.join(nod.xpath('.//div[@class="top_space contentAdjustmentBingon"]/span[not(@*)]/text()')).replace('  ', ' ')
			device_img = ''.join(nod.xpath('.//img[@class="deviceImg"]/@src'))
			if device_img:
				device_img = 'https:%s' % device_img
			values = [due_amount, due_date, logged_usernam, autopay, next_payment_schedule, name_, msisdn_, plan_type_, plan_name_, billing_pastdue, billing_talk_minutes, billing_txt_msg, billing_data_speed, bing_on_desc, device_img]
			csv_file.writerow(values)
		driver.find_element_by_xpath('//a[@id="logout-Ok"]').click()

        def is_path_file_name(self, excel_file_name):
                if os.path.isfile(excel_file_name):
                        os.system('rm %s' % excel_file_name)
                oupf = open(excel_file_name, 'ab+')
                todays_excel_file = csv.writer(oupf)
                return todays_excel_file

if __name__ == '__main__':
	obj = Tmobile()
	obj.main()
