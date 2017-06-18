# -*- coding: utf-8 -*-

import re
import json
from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from cnblogs.items import *

class CnblogsSpider(CrawlSpider):
    #�������������
    name = "CnblogsSpider"
    #��������ץȡ������,��������ڴ��б�����������ץȡ
    allowed_domains = ["cnblogs.com"]
    #����ץȡ�����url
    start_urls = [
        "http://www.cnblogs.com/rwxwsblog/default.html?page=1"
    ]
    # ������ȡURL�Ĺ��򣬲�ָ���ص�����Ϊparse_item
    rules = [
        Rule(sle(allow=("/rwxwsblog/default.html\?page=\d{1,}")), #�˴�Ҫע��?�ŵ�ת�������ƹ�����Ҫ��?�Ž���ת�塣
                         follow=True,
                         callback='parse_item')
    ]
    #print "**********CnblogsSpider**********"
    #����ص�����
    #��ȡ���ݵ�Items���棬��Ҫ�õ�XPath��CSSѡ������ȡ��ҳ����
    def parse_item(self, response):
        #print "-----------------"
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)
        postTitle = sel.css('div.day div.postTitle')
        #print "=============length======="
        postCon = sel.css('div.postCon div.c_b_p_desc')
        #���⡢url�������Ľṹ��һ����ɢ�Ľṹ�����ڿ��ԸĽ�
        for index in range(len(postTitle)):
            item = CnblogsItem()
            item['title'] = postTitle[index].css("a").xpath('text()').extract()[0]
            #print item['title'] + "***************\r\n"
            item['link'] = postTitle[index].css('a').xpath('@href').extract()[0]
            item['listUrl'] = base_url
            item['desc'] = postCon[index].xpath('text()').extract()[0]
            #print base_url + "********\n"
            items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'
        return items