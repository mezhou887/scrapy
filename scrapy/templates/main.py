from scrapy import cmdline
		
    # http://blog.csdn.net/winterto1990/article/details/52003045
	# https://zhuanlan.zhihu.com/p/26501250
 		
    # templatespider:  ������
    # template_data�� ������������
     
	cmdline.execute("scrapy crawl templatespider".split());                                                                                                                              
    # �־û�һ�����棬ʹ������ͣ/������ȡ,��ȫ��ֹͣ����(�� Ctrl-C ���߷���һ���ź�)                                  
    cmdline.execute("scrapy crawl templatespider -s JOBDIR=crawls/templatespider-1".split());
                                                                                             
    # ����Json, xml, csv�ļ�                                                              
    cmdline.execute("scrapy crawl templatespider -o template_data.json".split());           
    cmdline.execute("scrapy crawl templatespider -o template_data.jsonlines".split());      
    cmdline.execute("scrapy crawl templatespider -o template_data.xml".split());            
    cmdline.execute("scrapy crawl templatespider -o template_data.csv".split());            