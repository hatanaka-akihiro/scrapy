import os
import requests
from requests.auth import HTTPBasicAuth
import json
import urllib
from pathlib import Path
import logging

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, handlers=[stream_handler])

USER = os.environ.get('ZENDESK_USER')
TOKEN = os.environ.get('ZENDESK_TOKEN')


def get_articles():
    list_path = './urls_zendesk.txt'
    with open(list_path, 'w') as file:
        url = 'https://questetra.zendesk.com/api/v2/help_center/ja/articles.json?page[size]=100'
        while True:
            response = requests.get(url, auth=HTTPBasicAuth(USER + '/token', TOKEN))
            if response.status_code != 200:
                raise ValueError('response.status_code: {}'.format(response.status_code))
            jsonObj = json.loads(response.text)
            articles = jsonObj['articles']
            logging.info('articles.length: %d', len(articles))
            for article in articles:
                logging.info('id: %d, url: %s', article['id'], article['html_url'])
                file.write(article['html_url'] + '\n')
                save_body(article['html_url'], article['body'])
            if jsonObj['meta']['has_more'] != True:
                break
            url = jsonObj['links']['next']

def save_body(url, body):
    # レスポンスを保存するファイルパスを決定
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.netloc + '/' + parsed_url.path
    if path.endswith('/'):
        path = path.substring(0, path.length - 1) + '.html'
    elif path.endswith('.html') == False:
        path = path + '.html'
    path = './data/' + path
    logging.info('path: %s', path)

    file_path = Path(path)
    # ディレクトリが存在しない場合に作成する
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # ファイルに書き込む
    with file_path.open("w") as file:
        file.write(body)

get_articles()