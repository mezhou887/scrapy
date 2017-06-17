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

    # process_request 在请求传递给下载器前可以处理请求对象
    # 当每个request通过下载中间件时，该方法被调用。
    # 必须返回以下其中之一：一个 None 、一个 Response 对象、一个 Request 对象或 raise IgnoreRequest:
    #	 	如果其返回None ，Scrapy将继续处理该request，执行其他的中间件的相应方法，直到合适的下载器处理函数(download handler)被调用，该request被执行(其response被下载)。
    # 	如果其返回Response对象，Scrapy将不会调用任何其他中间件的process_request()或process_exception()方法，或相应地下载函数；其将返回该response。已安装的中间件的 process_response()方法则会在每个response返回时被调用。
    #		如果其返回Request对象，Scrapy则停止调用process_request方法并重新调度返回的request。当新返回的request被执行后，相应地中间件链将会根据下载的response被调用。
    # 	如果其raise一个 IgnoreRequest 异常，则安装的下载中间件的 process_exception() 方法会被调用。如果没有任何一个方法处理该异常，则request的errback(Request.errback)方法会被调用。如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。
    def process_request(self, request, spider):
        self.stats.inc_value('downloader/request_count', spider=spider)
        self.stats.inc_value('downloader/request_method_count/%s' % request.method, spider=spider)
        reqlen = len(request_httprepr(request))
        self.stats.inc_value('downloader/request_bytes', reqlen, spider=spider)


    # process_response 在响应传递给引擎前处理响应数据
    # 当下载器完成http请求，传递响应给引擎的时候调用
    # 必须返回以下其中之一: 返回一个 Response 对象、 返回一个 Request 对象或raise一个 IgnoreRequest 异常。
    #  如果其返回一个 Response (可以与传入的response相同，也可以是全新的对象)， 该response会被在链中的其他中间件的 process_response() 方法处理。
    #  如果其返回一个 Request 对象，则中间件链停止， 返回的request会被重新调度下载。处理类似于 process_request() 返回request所做的那样。
    #  如果其抛出一个 IgnoreRequest 异常，则调用request的errback(Request.errback)。 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)。
    def process_response(self, request, response, spider):
        self.stats.inc_value('downloader/response_count', spider=spider)
        self.stats.inc_value('downloader/response_status_count/%s' % response.status, spider=spider)
        reslen = len(response_httprepr(response))
        self.stats.inc_value('downloader/response_bytes', reslen, spider=spider)
        return response

    # process_exception 处理异步调用时发生的异常情况
    # 返回以下之一： 返回None 、一个 Response 对象、或者一个 Request 对象。
    #	 	如果其返回None，Scrapy 将会继续处理该异常，接着调用已安装的其他中间件的 process_exception()方法，直到所有中间件都被调用完毕，则调用默认的异常处理。
    #		如果其返回一个Response 对象，则已安装的中间件链的process_response()方法被调用。Scrapy 将不会调用任何其他中间件的 process_exception() 方法。
    #   如果其返回一个Request对象，则返回的request将会被重新调用下载。这将停止中间件的 process_exception()方法执行，就如返回一个 response 的那样。
    def process_exception(self, request, exception, spider):
        ex_class = global_object_name(exception.__class__)
        self.stats.inc_value('downloader/exception_count', spider=spider)
        self.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)
