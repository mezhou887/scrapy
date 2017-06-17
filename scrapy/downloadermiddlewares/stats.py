from scrapy.exceptions import NotConfigured
from scrapy.utils.request import request_httprepr
from scrapy.utils.response import response_httprepr
from scrapy.utils.python import global_object_name


class DownloaderStats(object):

    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('DOWNLOADER_STATS'):
            raise NotConfigured
        return cls(crawler.stats)

    # process_request �����󴫵ݸ�������ǰ���Դ����������
    # ��ÿ��requestͨ�������м��ʱ���÷��������á�
    # ���뷵����������֮һ��һ�� None ��һ�� Response ����һ�� Request ����� raise IgnoreRequest:
    #	 	����䷵��None ��Scrapy�����������request��ִ���������м������Ӧ������ֱ�����ʵ�������������(download handler)�����ã���request��ִ��(��response������)��
    # 	����䷵��Response����Scrapy����������κ������м����process_request()��process_exception()����������Ӧ�����غ������佫���ظ�response���Ѱ�װ���м���� process_response()���������ÿ��response����ʱ�����á�
    #		����䷵��Request����Scrapy��ֹͣ����process_request���������µ��ȷ��ص�request�����·��ص�request��ִ�к���Ӧ���м��������������ص�response�����á�
    # 	�����raiseһ�� IgnoreRequest �쳣����װ�������м���� process_exception() �����ᱻ���á����û���κ�һ������������쳣����request��errback(Request.errback)�����ᱻ���á����û�д��봦���׳����쳣������쳣�������Ҳ���¼(��ͬ�������쳣����)��
    def process_request(self, request, spider):
        self.stats.inc_value('downloader/request_count', spider=spider)
        self.stats.inc_value('downloader/request_method_count/%s' % request.method, spider=spider)
        reqlen = len(request_httprepr(request))
        self.stats.inc_value('downloader/request_bytes', reqlen, spider=spider)


    # process_response ����Ӧ���ݸ�����ǰ������Ӧ����
    # �����������http���󣬴�����Ӧ�������ʱ�����
    # ���뷵����������֮һ: ����һ�� Response ���� ����һ�� Request �����raiseһ�� IgnoreRequest �쳣��
    #  ����䷵��һ�� Response (�����봫���response��ͬ��Ҳ������ȫ�µĶ���)�� ��response�ᱻ�����е������м���� process_response() ��������
    #  ����䷵��һ�� Request �������м����ֹͣ�� ���ص�request�ᱻ���µ������ء����������� process_request() ����request������������
    #  ������׳�һ�� IgnoreRequest �쳣�������request��errback(Request.errback)�� ���û�д��봦���׳����쳣������쳣�������Ҳ���¼(��ͬ�������쳣����)��
    def process_response(self, request, response, spider):
        self.stats.inc_value('downloader/response_count', spider=spider)
        self.stats.inc_value('downloader/response_status_count/%s' % response.status, spider=spider)
        reslen = len(response_httprepr(response))
        self.stats.inc_value('downloader/response_bytes', reslen, spider=spider)
        return response

    # process_exception �����첽����ʱ�������쳣���
    # ��������֮һ�� ����None ��һ�� Response ���󡢻���һ�� Request ����
    #	 	����䷵��None��Scrapy �������������쳣�����ŵ����Ѱ�װ�������м���� process_exception()������ֱ�������м������������ϣ������Ĭ�ϵ��쳣����
    #		����䷵��һ��Response �������Ѱ�װ���м������process_response()���������á�Scrapy ����������κ������м���� process_exception() ������
    #   ����䷵��һ��Request�����򷵻ص�request���ᱻ���µ������ء��⽫ֹͣ�м���� process_exception()����ִ�У����緵��һ�� response ��������
    def process_exception(self, request, exception, spider):
        ex_class = global_object_name(exception.__class__)
        self.stats.inc_value('downloader/exception_count', spider=spider)
        self.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)
