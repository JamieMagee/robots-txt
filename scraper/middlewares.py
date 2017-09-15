from random import choice

from scrapy.downloadermiddlewares.retry import RetryMiddleware

COMMON_PREFIXES = {'http://', 'https://', 'http://www.', 'https://www.'}


class PrefixRetryMiddleware(RetryMiddleware):
    def process_exception(self, request, exception, spider):
        prefixes_tried = request.meta['prefixes']
        if COMMON_PREFIXES == prefixes_tried:
            return exception

        new_prefix = choice(tuple(COMMON_PREFIXES - prefixes_tried))
        request = self.add_prefix(request, new_prefix)

        return self._retry(request, exception, spider)

    @staticmethod
    def add_prefix(request, prefix):
        domain = request.meta['domain']
        meta = request.meta.copy()
        meta['prefixes'].add(prefix)

        request = request.replace(
            url=prefix + domain + '/robots.txt',
            meta=meta
        )

        return request
