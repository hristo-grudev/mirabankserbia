import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import MirabankserbiaItem
from itemloaders.processors import TakeFirst


class MirabankserbiaSpider(scrapy.Spider):
	name = 'mirabankserbia'
	start_urls = ['https://www.mirabankserbia.com/rs/news/']

	def parse(self, response):
		post_links = response.xpath('//a[text()="Detaljnije"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="Go to next page"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[contains(@class, "field-name-title")]/h2/text()').get()
		description = response.xpath('//div[@class="body field"]//text()[normalize-space()]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[contains(@class, "field-name-post-date")]/text()').get()

		item = ItemLoader(item=MirabankserbiaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
