import scrapy
import urllib
from pathlib import Path
import logging

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, handlers=[stream_handler])


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # 各リクエスト間に3秒の遅延
        'RETRY_TIMES': 5,     # リクエストが失敗した場合に最大5回まで再試行
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # 同時に2つのリクエストを送信
    }
    def start_requests(self):
        # テキストファイルのパス
        list_path = 'urls.txt'

        # ファイルを開き、URLのリストを作成
        with open(list_path, 'r') as file:
            urls = [line.strip() for line in file]

        # 各URLに対してリクエストを発行
        for url in urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        parsed_url = urllib.parse.urlparse(response.url)
        path = parsed_url.path
        if path.endswith('/'):
            path += 'index.html'
        path = './data' + path
        logging.info('path: %s', path)

        file_path = Path(path)
        # ディレクトリが存在しない場合に作成する
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # ファイルに書き込む
        with file_path.open("wb") as file:
            file.write(response.body)
