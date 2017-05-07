import scrapy
from scrapy.crawler import CrawlerProcess
import RssSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

spider = RssSpider.RssSpider()

process.crawl(spider)
process.start() # the script will block here until the crawling is finished
