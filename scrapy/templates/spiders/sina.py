# -*- coding: utf-8 -*-

from Sina.items import SinaItem
import scrapy
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaSpider(scrapy.Spider):
    name= "sina"
    allowed_domains= ["sina.com.cn"]
    start_urls= [
       "http://news.sina.com.cn/guide/"
    ]

    def parse(self, response):
        items= []
        # ���д����url �� ����
        parentUrls = response.xpath('//div[@id=\"tab01\"]/div/h3/a/@href').extract()
        parentTitle = response.xpath("//div[@id=\"tab01\"]/div/h3/a/text()").extract()

        # ����С���ur �� ����
        subUrls  = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id=\"tab01\"]/div/ul/li/a/text()').extract()

        #��ȡ���д���
        for i in range(0, len(parentTitle)):
            # ָ������Ŀ¼��·����Ŀ¼��
            parentFilename = "./Data/" + parentTitle[i]

            #���Ŀ¼�����ڣ��򴴽�Ŀ¼
            if(not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            # ��ȡ����С��
            for j in range(0, len(subUrls)):
                item = SinaItem()

                # ��������title��urls
                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]

                # ���С���url�Ƿ���ͬ������url��ͷ������Ƿ���True (sports.sina.com.cn �� sports.sina.com.cn/nba)
                if_belong = subUrls[j].startswith(item['parentUrls'])

                # ������ڱ����࣬���洢Ŀ¼���ڱ�����Ŀ¼��
                if(if_belong):
                    subFilename =parentFilename + '/'+ subTitle[j]
                    # ���Ŀ¼�����ڣ��򴴽�Ŀ¼
                    if(not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    # �洢 С��url��title��filename�ֶ�����
                    item['subUrls'] = subUrls[j]
                    item['subTitle'] =subTitle[j]
                    item['subFilename'] = subFilename

                    items.append(item)

        #����ÿ��С��url��Request���󣬵õ�Response��ͬ����meta���� һͬ�����ص����� second_parse ��������
        for item in items:
            yield scrapy.Request( url = item['subUrls'], meta={'meta_1': item}, callback=self.second_parse)

    #���ڷ��ص�С���url���ٽ��еݹ�����
    def second_parse(self, response):
        # ��ȡÿ��Response��meta����
        meta_1= response.meta['meta_1']

        # ȡ��С��������������
        sonUrls = response.xpath('//a/@href').extract()

        items= []
        for i in range(0, len(sonUrls)):
            # ���ÿ�������Ƿ��Դ���url��ͷ����.shtml��β������Ƿ���True
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

            # ������ڱ����࣬��ȡ�ֶ�ֵ����ͬһ��item�±��ڴ���
            if(if_belong):
                item = SinaItem()
                item['parentTitle'] =meta_1['parentTitle']
                item['parentUrls'] =meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)

        #����ÿ��С����������url��Request���󣬵õ�Response����ͬ����meta���� һͬ�����ص����� detail_parse ��������
        for item in items:
                yield scrapy.Request(url=item['sonUrls'], meta={'meta_2':item}, callback = self.detail_parse)

    # ���ݽ�����������ȡ���±��������
    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ""
        head = response.xpath('//h1[@id=\"main_title\"]/text()')
        content_list = response.xpath('//div[@id=\"artibody\"]/p/text()').extract()

        # ��p��ǩ����ı����ݺϲ���һ��
        for content_one in content_list:
            content += content_one

        item['head']= head
        item['content']= content

        yield item