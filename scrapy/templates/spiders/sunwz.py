# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Sunwz.items import SunwzItem


class SunwzSpider(CrawlSpider):
    name = 'sunwz'
    num = 0
    allow_domain = ['http://wz.sun0769.com/']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4']
    rules = {
        Rule(LinkExtractor(allow='page')),
        Rule(LinkExtractor(allow='/index\.php/question/questionType\?type=4$')),
        Rule(LinkExtractor(allow='/html/question/\d+/\d+\.shtml$'), follow = True, callback='parse_content')
    }

    xpathDict = {
        'title': '//div[contains(@class, "pagecenter p3")]/div/div/div[contains(@class,"cleft")]/strong/text()',
        'content': '//div[contains(@class, "c1 text14_2")]/text()',
        'content_first': '//div[contains(@class, "contentext")]/text()'
    }

    def parse_content(self, response):
        item = SunwzItem()
        content = response.xpath(self.xpathDict['content_first']).extract()
        if len(content) == 0:
            content = response.xpath(self.xpathDict['content']).extract()[0]
        else:
            content = content[0]
        title = response.xpath(self.xpathDict['title']).extract()[0]
        title_list = title.split(' ')
        number = title_list[-1]
        number = number.split(':')[-1]
        url = response.url
        item['url'] = url
        item['number'] = number
        item['title'] = title
        item['content'] = content

        yield item