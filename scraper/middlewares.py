from scrapy.downloadermiddlewares.retry import RetryMiddleware
from random import choice

from twisted.internet.error import DNSLookupError

COMMON_PREFIXES = {'http://', 'https://', 'http://www.', 'https://www.'}


class PrefixRetryMiddleware(RetryMiddleware):

    def process_exception(self, request, exception, spider):
        prefixes_tried = request.meta['prefixes']
        if COMMON_PREFIXES == prefixes_tried:
            return exception
        domain = request.meta['domain']
        new_prefix = choice(tuple(COMMON_PREFIXES - prefixes_tried))
        request = request.replace(url=new_prefix + domain + '/robots.txt')
        return self._retry(request, exception, spider)