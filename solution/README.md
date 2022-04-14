# start

+ `docker-compose up -d`, `docker-compose down`

# kafka

+ `docker exec -it kafka /bin/bash`: логинимся в систему с kafka
+ `kafka-topics --create --topic algorithms-events --bootstrap-server localhost:9092`: создаем topic
+ `kafka-topics --describe --topic algorithms-events --bootstrap-server localhost:9092`: выводим инфу о топике
+ `kafka-console-consumer --topic algorithms-events --from-beginning --bootstrap-server localhost:9092`: показывает какие сообщения поступают

# kafka connect

+ `http://localhost:8083/connectors`: проверить кол-во коннекторов
+ `http://localhost:8083/connectors/sink-elastic-01/tasks/0/status`: посмотреть в каком статусе сейчас коннектор

# scrapy

Inside of scrapy project:

+ `scrapy crawl github -O github.json` write scrapy contents to github.json
+ `scrapy crawl github -o github.jl` write scrapy contents to github.jl (json list)
+ `scrapy crawl github -O github.json -a topic=ukkonen` pass command line arguments
+ `scrapy shell 'url'` open scrapy shell at url

# elastic search

+ `http://localhost:9200/algorithms-events/_search?pretty`: see events in topic

# monitoring

+ https://habr.com/ru/company/itsumma/blog/596845/

# safety

+ https://habr.com/ru/post/645733/

# Траблы

Была какая-то ебля с тем, что docker.elastic.co не выдавал образ elasticsearch,
поэтому нужно было самостоятельно его составлять. ПОсле этого была ебла с тем,
что es ничего не писал в логи, и нужно было исправлять аргументы (ES_JAVA_OPTS)
которые были даны в туторах.

Эта команда работает
`docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:6.5.0`

# TUTORS

## kafka connect

+ `https://medium.com/@raymasson/kafka-elasticsearch-connector-fa92a8e3b0bc`
   - `https://github.com/raymasson/kafka-elasticsearch-connector/blob/master/docker-compose.yml`
+ `https://rmoff.net/2019/10/07/kafka-connect-and-elasticsearch/`
   - `https://github.com/rmoff/kafka-elasticsearch/blob/master/docker-compose.yml`
