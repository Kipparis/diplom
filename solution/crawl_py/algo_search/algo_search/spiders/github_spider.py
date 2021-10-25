import scrapy
import json

class GithubSpider(scrapy.Spider):
    name = "github"

    def __init__(self, topic=None, *args, **kwargs):
        super(GithubSpider, self).__init__(*args, **kwargs)

        assert topic is not None, "you should provide topic variable via cmd"
        self.start_urls = [f"https://github.com/search?q={topic}"]


    def parse(self, response):
        # если есть следующая страница, запускаемся на следующей
        next_page = response.xpath('//a[@class="next_page"]/@href').get()
        if next_page is not None:
            # response.follow нативно поддерживает переход по относительным url
            yield response.follow(next_page, callback=self.parse)

        # находим репозитории на текущей странице
        repos_selector = response.xpath('//li[contains(@class, "repo-list-item")]'
                                        '//div[contains(@class, "text-normal")]'
                                        '/a')
        yield from response.follow_all(repos_selector, self.parse_repo)

    def parse_repo(self, response):
        # TODO:
        #   возможно закачивать на локальную папку уже готовые куски кода, или
        #   добавить опцию "сохранить", чтобы чел мог у себя в бразуере открыть
        #   это репо
        #
        #   можно добавить время когда последний раз обновился репозиторий
        #

        ### язык кода
        ### берем первый из списка, на проценты не смотрим
        language = response.xpath(
            '//h2[text() = "Languages"]/parent::div/ul/li/a/span/text()').get()

        ### about
        ### у каждого репо есть короткое описание о чем он
        about = response.xpath(
            '//h2[text() = "About"]/parent::div/p/text()').get()

        ### популярность (валидна для гитхаба)
        ### (при выводе для каждого сайта надо нормализовать)
        popularity = response.xpath(
            '//a[contains(@class, "social-count")]/text()').get()

        # change how yield works
        yield {'repo_url': response.url,
               'language': language,
               'about': about,
               'popularity': popularity}
