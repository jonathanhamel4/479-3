# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ConUSpider(CrawlSpider):
    name = "ConUSpider"
    allowed_domains = ["http://www.concordia.ca/artsci/"]
    start_urls = ['http://www.concordia.ca/artsci/biology.html']

    def parse(self, response):
        print response.url
        body = response.xpath('//body').extract();
        soup = BeautifulSoup(response.body)
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        print text
        return
