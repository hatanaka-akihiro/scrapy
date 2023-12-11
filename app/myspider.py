import scrapy
import os

class BlogSpider(scrapy.Spider):
    name = 'qspider'
    allowed_domains = ['support.questetra.com']
    start_urls = ['https://support.questetra.com/ja/']

    def parse(self, response):
        yield {
            'url': response.url,
            'title': response.css('title::text').get()
        }
        for href in response.css('a::attr(href)'):
            yield response.follow(href, callback=self.parse)
        #        yield scrapy.Request(next_page, callback=self.parse)
        #         output_path = '/app/data/'
        #         os.makedirs(os.path.dirname(output_path), exist_ok=True)
        #         with open(output_path + 'index.html', 'w', encoding='utf-8') as f:
        #             f.write(response.text)