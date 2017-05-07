import scrapy
from peewee import *
from scrapy.spiders.feed import XMLFeedSpider

db = SqliteDatabase('scrapy_triplets.db')

class BaseModel(Model):
    class Meta:
        database = db

class Scrapy_triplets_table(BaseModel):
    url = CharField(primary_key=True)
    title = CharField()
    description = CharField()

Scrapy_triplets_table.create_table(True)

class RssSpider(XMLFeedSpider):
	name='newsspider'
	start_urls = ['https://lenta.ru/rss']
	itertag = 'item'
	
	def parse_node(self, response, node):
		if node is None :
			return None
		# extract tuple
		title = node.xpath('title/text()').extract_first()
		descr = node.xpath('description/text()').extract_first()
		link = node.xpath('link/text()').extract_first()
		try:
			Scrapy_triplets_table.create(url=link, title=title, description=descr)
		except Exception:
			pass
		return None
