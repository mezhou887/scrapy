from scrapy import cmdline
		
    # http://blog.csdn.net/winterto1990/article/details/52003045
	# https://zhuanlan.zhihu.com/p/26501250
 		
    # templatespider:  爬虫名
    # template_data： 导出的数据名
     
	cmdline.execute("scrapy crawl templatespider".split());                                                                                                                              
    # 持久化一个爬虫，使它能暂停/继续爬取,安全地停止爬虫(按 Ctrl-C 或者发送一个信号)                                  
    cmdline.execute("scrapy crawl templatespider -s JOBDIR=crawls/templatespider-1".split());
                                                                                             
    # 导出Json, xml, csv文件                                                              
    cmdline.execute("scrapy crawl templatespider -o template_data.json".split());           
    cmdline.execute("scrapy crawl templatespider -o template_data.jsonlines".split());      
    cmdline.execute("scrapy crawl templatespider -o template_data.xml".split());            
    cmdline.execute("scrapy crawl templatespider -o template_data.csv".split());            