# -*- coding: utf-8 -*-

# Scrapy settings for SCOI project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'SCOI'

SPIDER_MODULES = ['SCOI.spiders']
NEWSPIDER_MODULE = 'SCOI.spiders'
ITEM_PIPELINES = {
            'SCOI.pipelines.ScoiPipeline': 300
}
DEFAULT_ITEM_CLASS = 'SCOI.items.SCOI'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SCOI (+http://www.yourdomain.com)'
