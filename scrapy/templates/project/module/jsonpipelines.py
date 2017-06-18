import json
import codecs

# ITEM_PIPELINES = {                                           
#     'cnblogs.pipelines.JsonWithEncodingPipeline': 300,
# } 

# ��Spider��parse���ص�Item���ݽ����α�ITEM_PIPELINES�б��е�Pipeline�ദ��                                                           
class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('sunwz.json', 'w', encoding='utf-8');  # ����ץȡ��items����JSON��ʽ�������������ɵ�sunwz.json�ļ��С�

    # process_item(item, spider)Ϊÿ��item pipeline ������ã�������Ҫ����һ��scrapy.item.Itemʵ����������׳�һ��?scrapy.exceptions.DropItem�쳣�����׳��쳣��� item �����ᱻ֮���pipeline ����
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n";
        self.file.write(line);
        return item;

    #  �������֮�󱻵���: open_spider(spider) 
    #  ������ر�֮�󱻵���: close_spider(spider)
    def spider_closed(self, spider):
        self.file.close();