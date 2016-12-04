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
import scraper.indexer.indexerscript
reload(sys)
sys.setdefaultencoding('utf-8')

class ConUSpider(CrawlSpider):
    name = "ConUSpider"
    allowed_domains = ['concordia.ca']
    start_urls = ['http://www.concordia.ca/artsci/physics.html', 'http://www.concordia.ca/artsci/chemistry.html', 'http://www.concordia.ca/artsci/biology.html', 'http://www.concordia.ca/artsci/geography-planning-environment.html', 'http://www.concordia.ca/artsci/math-stats.html', 'http://www.concordia.ca/artsci/psychology.html', 'http://www.concordia.ca/artsci/science-college.html', 'http://www.concordia.ca/artsci/exercise-science.html']
    rules = (
                Rule(LinkExtractor(allow=('(concordia.ca/artsci/exercise-science/)')), callback='parse_start_url', follow=True),
                Rule(LinkExtractor(allow=('(concordia.ca/artsci/physics/)')), callback='parse_start_url', follow=True),
                Rule(LinkExtractor(allow=('(concordia.ca/artsci/chemistry/)')), callback='parse_start_url', follow=True),
                Rule(LinkExtractor(allow=('(concordia.ca/artsci/biology/)')), callback='parse_start_url', follow=True),
                Rule(LinkExtractor(allow=('(concordia.ca/artsci/geography-planning-environment/)')), callback='parse_start_url', follow=True),
                Rule(LinkExtractor(allow=('(concordia.ca/artsci/math-stats/)')), callback='parse_start_url', follow=True),
                Rule(LinkExtractor(allow=('(concordia.ca/artsci/psychology/)')), callback='parse_start_url', follow=True),
                Rule(LinkExtractor(allow=('(concordia.ca/artsci/science-college/)')), callback='parse_start_url', follow=True),
            )
    links = []
    count = 3080
    isDebug = False

    def get_dept_id(self, url):
        deptId = None
        if bool(re.search("artsci\/biology", url)):
            deptId = 1
        elif bool(re.search("artsci\/chemistry", url)):
            deptId = 2
        elif bool(re.search("artsci\/exercise-science", url)):
            deptId = 3
        elif bool(re.search("artsci\/geography-planning-environment", url)):
            deptId = 4
        elif bool(re.search("artsci\/math-stats", url)):
            deptId = 5
        elif bool(re.search("artsci\/physics", url)):
            deptId = 6
        elif bool(re.search("artsci\/psychology", url)):
            deptId = 7
        elif bool(re.search("artsci\/science-college", url)):
            deptId = 8
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

        try:
            deptId = self.get_dept_id(response.url)
            if deptId is not None:
                scraper.afinn.afinnscript.getAfinnScore(chunks, str(deptId))

            scraper.indexer.indexerscript.indexDocument(chunks, self.count, response.url)
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
        return

    def spider_closed(self, spider):
        print "CLOSING SPIDER"
        print str(self.count)
      # second param is instance of spder about to be closed.
