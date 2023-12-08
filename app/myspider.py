import scrapy
import os

class BlogSpider(scrapy.Spider):
    name = 'qspider'
    allowed_domains = ['support.questetra.com']
    start_urls = ['https://support.questetra.com/']

    def parse(self, response):
        output_path = '/app/data/'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path + 'index.html', 'w', encoding='utf-8') as f:
            f.write(response.text)