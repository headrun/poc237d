start_urls_list = ['https://www.fbi.gov/wanted']
fields_list = ["Name", "URL", "Alias", "Remarks", "Caution" , "Citizenship"]
category_urls_list = '//ul[@class="inline-list section-menu"]//li//a//@href'
per_page_results_terrorism = '//p[@class="read-more text-center bottom-total visualClear"]/text()'
complete_url_terrorism = "https://www.fbi.gov/wanted/terrorism/@@castle.cms.querylisting/55d8265003c84ff2a7688d7acd8ebd5a?page="
per_page_results_vicap = '//p[@class="read-more text-center bottom-total visualClear"]/text()'
complete_url_vicap = "https://www.fbi.gov/wanted/vicap/@@castle.cms.querylisting/querylisting-1?page="
per_page_results_seeking_information = '//p[@class="read-more text-center bottom-total visualClear"]/text()'
complete_url_seeking_information = "https://www.fbi.gov/wanted/seeking-information/@@castle.cms.querylisting/5abe9de716674277b799bc03b34e1aa4?page="
per_page_results_wanted_kidnap = '//p[@class="read-more text-center bottom-total visualClear"]/text()'
complete_url_wanted_kidnap = "https://www.fbi.gov/wanted/kidnap/@@castle.cms.querylisting/querylisting-1?page="
name_url_nodes_topten = '//div[@id="query-results-0f737222c5054a81a120bce207b0446a"]//ul//li'
name_topten = './h3/a//text()'
each_url_topten = './h3/a/@href'
per_page_results_fugitives = '//p[@class="read-more text-center bottom-total visualClear"]/text()'
complete_url_fugitives = "https://www.fbi.gov/wanted/fugitives/@@castle.cms.querylisting/f7f80a1681ac41a08266bd0920c9d9d8?page="
name_url_nodes_parental_kidnappings = '//div[@id="query-results-querylisting-1"]//ul//li'
name_parental_kidnappings = './h3/a//text()'
each_url_parental_kidnappings = './h3/a/@href'
name_url_nodes_bank_robbers = '//div[@class="query-results pat-pager"]//ul//li'
name_bank_robbers = './p/a//text()'
each_url_bank_robbers = './p/a/@href'
name_url_nodes_ecap = '//div[@id="query-results-querylisting-1"]//ul//li'
name_ecap = './h3/a//text()'
each_url_ecap = './h3/a/@href'
name_url_nodes_all_names = '//div[@class="query-results pat-pager"]//ul//li'
name_all_names = './p/a//text()'
name_allnames = './h3/a//text()'
each_url_all_names = './p/a/@href'
each_url_allnames = './h3/a/@href'
aliases_detail = '//section[@id="content-core"]//div[@class="wanted-person-aliases"]/p//text()'
remarks_detail = '//section[@id="content-core"]//div[@class="wanted-person-remarks"]/p//text()'
caution_detail = '//section[@id="content-core"]//div[@class="wanted-person-caution"]/p//text()'
nationality_detail = '//table[@class="table table-striped wanted-person-description"]//td[contains(text(), "Nationality")]/following-sibling::td//text()'
