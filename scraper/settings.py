BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3198.0 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

COOKIES_ENABLED = False
TELNETCONSOLE_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 4
RETRY_HTTP_CODES = range(999)
CONCURRENT_REQUESTS = 100
REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'INFO'
DOWNLOAD_TIMEOUT = 15

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scraper.middlewares.PrefixRetryMiddleware': 551,
}
