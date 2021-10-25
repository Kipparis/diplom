# usage

+ `scrapy crawl github -O github.json` write scrapy contents to github.json
+ `scrapy crawl github -o github.jl` write scrapy contents to github.jl (json list)
+ `scrapy crawl github -O github.json -a topic=ukkonen` pass command line arguments
+ `scrapy shell 'url'` open scrapy shell at url

# why scrapy

+ by default filters out diplicated requests to URLs already visited
