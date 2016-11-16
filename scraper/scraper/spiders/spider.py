# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ConUSpider(CrawlSpider):
    name = "ConUSpider"
    allowed_domains = ['concordia.ca']
    start_urls = ['http://www.concordia.ca/artsci/physics.html']
    rules = (Rule(LinkExtractor(allow=('(concordia.ca/artsci/physics/)')), callback='parse_start_url', follow=True),)
    links = []
    count = 0
    isDebug = False

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ConUSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse_start_url(self, response):
        self.count = self.count + 1
        print response.url
        self.links.append(response.url)
        if self.isDebug is True and self.count > 50:
            raise CloseSpider('Max number')
        #Use the following to extract html from the link and then parse it.
        # if len(links) > 3:
        #     raise CloseSpider('Max number of pages exceded')
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
        print "PRINTING"
        print str(self.count)
      # second param is instance of spder about to be closed.