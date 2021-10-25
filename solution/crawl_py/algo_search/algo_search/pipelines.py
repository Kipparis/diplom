# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from kafka import KafkaProducer
import json

class AlgoSearchPipeline:

    def __init__(self, kafka_bootstrap_server, kafka_topic):
        self.kafka_bootstrap_server = kafka_bootstrap_server
        self.kafka_topic = kafka_topic

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            kafka_bootstrap_server=crawler.settings.get('KAFKA_BOOTSTRAP_SERVER'),
            kafka_topic=crawler.settings.get('KAFKA_TOPIC')
        )

    def open_spider(self, spider):
        # doc: https://towardsdatascience.com/kafka-python-explained-in-10-lines-of-code-800e3e07dad1
        self.producer = KafkaProducer(
            bootstrap_servers=[self.kafka_bootstrap_server],
            value_serializer=lambda val: json.dumps(val,ensure_ascii=False).encode('utf-8'))

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # check if it has some forbidden keywords
        payload = dict(item)
        payload.update({"spider_name": spider.name,
                        "start_urls": spider.start_urls})
        self.producer.send(self.kafka_topic, value=payload)
        return item
