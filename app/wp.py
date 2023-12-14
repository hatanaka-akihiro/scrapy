import os
import requests
import urllib
import json
from pathlib import Path
import logging

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, handlers=[stream_handler])

API_TOKEN = os.environ.get('API_TOKEN')

API_VERSION = 'v1.1'
DOMAIN = 'support.questetra.com'

HEADERS = {'Authorization': 'Bearer {}'.format(API_TOKEN)}


def get_posts():
    list_path = './urls_wordpress.txt'
    with open(list_path, 'w') as file:
        number = 100
        url = 'https://public-api.wordpress.com/rest/{}/sites/{}/posts/?order=ASC&order_by=ID&fields=ID,URL,content&status=publish&number={}'.format(
            API_VERSION, DOMAIN, number
        )
        logging.info('url: %s', url)
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise ValueError('response.status_code: {}'.format(response.status_code))

        jsonObj = json.loads(response.text)
        posts = jsonObj['posts']
        logging.info('found: %d, posts.length: %d, first: %d', jsonObj['found'], len(posts), posts[0]['ID'])
        for post in posts:
            file.write(post['URL'] + '\n')
            save_body(post['URL'], post['content'])
        return

        while 'next_page' in jsonObj['meta']:
            next_page = jsonObj['meta']['next_page']
            nextUrl = url + '&page_handle=' + urllib.parse.quote(next_page)
            logging.info('url: %s', nextUrl)
            response = requests.get(nextUrl, headers=HEADERS)
            if response.status_code != 200:
                raise ValueError('response.status_code: {}'.format(response.status_code))

            jsonObj = json.loads(response.text)
            posts = jsonObj['posts']
            logging.info('posts.length: %d, first: %d', len(posts), posts[0]['ID'])
            for post in posts:
                file.write(post['URL'] + '\n')
                save_body(post['URL'], post['content'])

def save_body(url, body):
    # レスポンスを保存するファイルパスを決定
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.netloc + parsed_url.path
    if path.endswith('/'):
        path = path[:-1] + '.html'
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

get_posts()