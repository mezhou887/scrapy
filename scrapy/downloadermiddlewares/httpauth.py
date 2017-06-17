"""
HTTP basic auth downloader middleware

See documentation in docs/topics/downloader-middleware.rst
"""

from w3lib.http import basic_auth_header

from scrapy import signals

# 完成某些使用 Basic access authentication (或者叫HTTP认证)的spider生成的请求的认证过程。
class HttpAuthMiddleware(object):
    """Set Basic HTTP Authorization header
    (http_user and http_pass spider class attributes)"""

    @classmethod
    def from_crawler(cls, crawler):
        o = cls()
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def spider_opened(self, spider):
        usr = getattr(spider, 'http_user', '')
        pwd = getattr(spider, 'http_pass', '')
        if usr or pwd:
            self.auth = basic_auth_header(usr, pwd)

    def process_request(self, request, spider):
        auth = getattr(self, 'auth', None)
        if auth and b'Authorization' not in request.headers:
            request.headers[b'Authorization'] = auth
