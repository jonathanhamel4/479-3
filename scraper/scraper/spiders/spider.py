# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import signals
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
import sys
import scraper.afinn.afinnscript
import re
reload(sys)
sys.setdefaultencoding('utf-8')

class ConUSpider(CrawlSpider):
    name = "ConUSpider"
    allowed_domains = ['concordia.ca']
    start_urls = ['http://www.concordia.ca/artsci/physics.html']
    #rules = (Rule(LinkExtractor(allow=('(concordia.ca/artsci/physics/)')), callback='parse_start_url', follow=True),)
    links = []
    count = 0
    isDebug = False

    @classmethod
    def get_dept_id(url):
        print "HERE"
        deptId = None
        if bool(re.search(url, "artsci\/biology")):
            deptId = 1
        elif bool(re.search(url, "artsci\/chemistry")):
            deptId = 2
        elif bool(re.search(url, "artsci\/exercise-science")):
            deptId = 3
        elif bool(re.search(url, "artsci\/geography-planning-environment")):
            deptId = 4
        elif bool(re.search(url, "artsci\/math-stats")):
            deptId = 5
        elif bool(re.search(url, "artsci\/physics")):
            deptId = 6
        elif bool(re.search(url, "artsci\/psychology")):
            deptId = 7
        elif bool(re.search(url, "artsci\/science-college")):
            deptId = 8
        print str(deptId)
        return deptId

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ConUSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def parse_start_url(self, response):
        self.count = self.count + 1
        print response.url
        self.links.append(response.url)
        if self.isDebug is True and self.count > 1:
            raise CloseSpider('')
        #Use the following to extract html from the link and then parse it.
        #body = response.xpath('//body').extract(); #-> Takes headers, body, footer
        #description = response.xpath('//html/head/meta[@http-equiv="description"]/@content').extract()[0]
        body = response.xpath('//section[@id="content-main"]/div[@class="container"]').extract() #-> Takes only the content
        soup = BeautifulSoup(response.body)
        for a in soup.findAll('a'):
            del a['href']
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = " ".join(list(filter(None, list((phrase.strip() for line in lines for phrase in line.split("  "))))))
        # drop blank lines
        try:
            self.get_dept_id(response.url)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise

        #scraper.afinn.afinnscript.getAfinnScore(chunks, self.getDeptId(response.url))

        # THEN INDEX
        return

    def spider_closed(self, spider):
        print "CLOSING SPIDER"
        print str(self.count)
      # second param is instance of spder about to be closed.
