from selenium import webdriver
from base64 import b64encode
import time
from scrapy.selector import Selector


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


class Xfinity():
	def main(self):
		driver = get_proxy_driver('96.44.146.106', '6060')
		#driver  = get_proxy_driver('47.206.51.67', '8080')
		driver.get('https://login.xfinity.com/login?r=comcast.net&s=oauth&continue=https%3A%2F%2Foauth.xfinity.com%2Foauth%2Fauthorize%3Fclient_id%3Dmy-account-web%26prompt%3Dlogin%26redirect_uri%3Dhttps%253A%252F%252Fcustomer.xfinity.com%252Foauth%252Fcallback%26response_type%3Dcode%26state%3D%2523%252F%26response%3D1&forceAuthn=1&client_id=my-account-web')
		time.sleep(5)
		driver.find_element_by_xpath('//input[@id="user"]').clear()
		driver.find_element_by_xpath('//input[@id="user"]').send_keys("frosts107@comcast.net")
		driver.find_element_by_xpath('//input[@id="passwd"]').clear()
		driver.find_element_by_xpath('//input[@id="passwd"]').send_keys("Marchbaby2017")
		driver.find_element_by_xpath('//button[@id="sign_in"]').click()
		time.sleep(10)
		sel = Selector(text=driver.page_source)
		billing_heading = ''.join(sel.xpath('//span[@class="heading3"]//text()').extract())
		fp = open('xfinity-data.txt', 'a')
		fp.write(billing_heading.strip()+'\n')
		bill_click = driver.find_element_by_xpath('//a[contains(text(), "View Billing")]').click()
		time.sleep(10)
		sel = Selector(text=driver.page_source)
		nodes = sel.xpath('//ul[@class="list--no-bullets"]//li')
		for node in nodes:
			fp.write(''.join(node.xpath('.//text()').extract()).strip()+'\n')
		#driver.find_element_by_xpath('//a[contains(text(), "View Bill Details (PDF)")]').click()
		sel_view  = Selector(text=driver.page_source)	
		url =  ''.join(sel_view.xpath('//a[contains(text(), "View Bill Details (PDF)")]/@href').extract())
		bill_url  = "https://customer.xfinity.com/"+url
		driver.get(bill_url)
		driver.save_screenshot('bill-image.png')	

if __name__ == '__main__':
	obj = Xfinity()
	obj.main()
	

