import json
import codecs

# ITEM_PIPELINES = {                                           
#     'cnblogs.pipelines.JsonWithEncodingPipeline': 300,
# }                                                            
class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('sunwz.json', 'w', encoding='utf-8');

    # process_item(item, spider)为每个item pipeline 组件调用，并且需要返回一个scrapy.item.Item实例对象或者抛出一个?scrapy.exceptions.DropItem异常。当抛出异常后该 item 将不会被之后的pipeline 处理。
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n";
        self.file.write(line);
        return item;

    #  当爬虫打开之后被调用: open_spider(spider) 
    #  当爬虫关闭之后被调用。
    def spider_closed(self, spider):
        self.file.close();