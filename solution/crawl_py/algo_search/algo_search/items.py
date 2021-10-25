# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlgoSearchItem(scrapy.Item):
    repo_url = scrapy.Field()
    language = scrapy.Field()
    about = scrapy.Field()
    popularity = scrapy.Field()
