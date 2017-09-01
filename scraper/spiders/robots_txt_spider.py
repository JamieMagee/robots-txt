import csv
import os

import scrapy

DOWNLOAD_DIR = 'robots-txt'
TOP_LIST = 'top-1m.csv'


class RobotsTxtSpider(scrapy.Spider):
    name = 'robots'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parent_dir = os.path.join(os.path.dirname(__file__), os.pardir)
        if not os.path.exists(os.path.join(self.parent_dir, DOWNLOAD_DIR)):
            os.makedirs(os.path.join(self.parent_dir, DOWNLOAD_DIR))

    def start_requests(self):
        with open(os.path.join(self.parent_dir, TOP_LIST)) as csv_file:
            cr = csv.reader(csv_file)
            for domain in cr:
                if self.downloaded(domain[1]):
                    continue
                req = scrapy.Request('http://www.' + domain[1] + '/robots.txt',
                                     callback=self.parse)
                req.meta['domain'] = domain[1]
                req.meta['prefixes'] = {'http://www.'}
                yield req

    def parse(self, response):
        name = response.request.meta['domain']
        if not RobotsTxtSpider.valid_response(response):
            return
        with open(os.path.join(self.parent_dir, DOWNLOAD_DIR, name), 'w') as f:
            f.write(response.text)

    def downloaded(self, domain):
        full_path = os.path.join(self.parent_dir, DOWNLOAD_DIR, domain)
        if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
            return True
        return False

    @staticmethod
    def valid_response(response):
        content_type = response.headers.get('Content-Type')
        if content_type is None:
            return response.status == 200 and \
                   len(response.text) != 0
        else:
            return content_type is not None and \
                   'text/plain' in content_type.decode() and \
                   response.status == 200 and \
                   len(response.text) != 0
