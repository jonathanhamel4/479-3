# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

links = []
class ConUSpider(CrawlSpider):
    name = "ConUSpider"
    allowed_domains = ['concordia.ca']
    start_urls = ['http://www.concordia.ca/artsci/biology.html']
    rules = (Rule(LinkExtractor(allow=('(concordia.ca/artsci/biology)')), callback='parse_start_url', follow=True),)


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ConUSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse_start_url(self, response):
        print response.url
        links.append(response.url)
        # body = response.xpath('//body').extract();
        # soup = BeautifulSoup(response.body)
        # for script in soup(["script", "style"]):
        #     script.extract()
        # text = soup.get_text()
        # lines = (line.strip() for line in text.splitlines())
        # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # # drop blank lines
        # text = '\n'.join(chunk for chunk in chunks if chunk)
        # print text
        return

    def spider_closed(self, spider):
        print str(links)
      # second param is instance of spder about to be closed.
