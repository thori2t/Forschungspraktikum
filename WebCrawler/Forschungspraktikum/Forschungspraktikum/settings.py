# Scrapy settings for Forschungspraktikum project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "Forschungspraktikum"

SPIDER_MODULES = ["Forschungspraktikum.spiders"]
NEWSPIDER_MODULE = "Forschungspraktikum.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Forschungspraktikum (thoralf.teumer@s2021.tu-chemnitz.de)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1
REACTOR_THREADPOOL_MAXSIZE = 20
DNSCACHE_SIZE = 100000

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "Forschungspraktikum.middlewares.ForschungspraktikumSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "Forschungspraktikum.middlewares.ForschungspraktikumDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "Forschungspraktikum.pipelines.ForschungspraktikumPipeline": 1,
}
<<<<<<< HEAD
#IMAGES_STORE = '/run/media/thori2t/HDD_LUL/Forschungspraktikum/Images'
IMAGES_STORE = 'Images'
IMAGES_MIN_HEIGHT = 256
IMAGES_MIN_WIDTH = 256
=======
IMAGES_STORE = '/run/media/thori2t/HDD_LUL/Forschungspraktikum/Images'
IMAGES_MIN_HEIGHT = 100
IMAGES_MIN_WIDTH = 100
>>>>>>> ac11c2bf7721a92949310d3b5ab412c652d1fb41

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 30
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"


# Code von Claude
# Crawl begrenzen
DEPTH_LIMIT = 1
DOWNLOAD_TIMEOUT = 30
DOWNLOAD_MAXSIZE = 10 * 1024*1024
RETRY_TIMES = 2

# Domains abwechselnd statt eine nach der anderen abarbeiten
SCHEDULER_PRIORITY_QUEUE = "scrapy.pqueues.DownloaderAwarePriorityQueue"
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = "scrapy.squeues.PickleFifoDiskQueue"
SCHEDULER_MEMORY_QUEUE = "scrapy.squeues.FifoMemoryQueue"

# Komfort
LOG_LEVEL = "INFO"
JOBDIR = "crawls/run5"
