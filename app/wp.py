import requests
import urllib
import json
import logging
import os

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, handlers=[stream_handler])

API_TOKEN = os.environ.get('API_TOKEN')

API_VERSION = 'v1.1'
DOMAIN = 'support.questetra.com'

HEADERS = {'Authorization': 'Bearer {}'.format(API_TOKEN)}


def get_posts(category):
    post_ids = []
    url = 'https://public-api.wordpress.com/rest/{}/sites/{}/posts/?order=ASC&order_by=ID&fields=ID&status=publish&category={}'.format(
        API_VERSION, DOMAIN, category
    )
    logging.info('url: %s', url)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise ValueError('response.status_code: {}'.format(response.status_code))

    jsonObj = json.loads(response.text)
    posts = jsonObj['posts']
    logging.info('found: %d, posts.length: %d, first: %d', jsonObj['found'], len(posts), posts[0]['ID'])
    post_ids.extend([post['ID'] for post in posts])

    while 'next_page' in jsonObj['meta']:
        next_page = jsonObj['meta']['next_page']
        url = 'https://public-api.wordpress.com/rest/{}/sites/{}/posts/?order=ASC&order_by=ID&fields=ID&status=publish&category={}&page_handle={}'.format(
            API_VERSION, DOMAIN, category, urllib.parse.quote(next_page)
        )
        logging.info('url: %s', url)
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise ValueError('response.status_code: {}'.format(response.status_code))

        jsonObj = json.loads(response.text)
        posts = jsonObj['posts']
        logging.info('posts.length: %d, first: %d', len(posts), posts[0]['ID'])
        post_ids.extend([post['ID'] for post in posts])

    return post_ids


def get_post(post_id):
    url = 'https://public-api.wordpress.com/rest/{}/sites/{}/posts/{}'.format(
        API_VERSION, DOMAIN, post_id
    )
    logging.info('url: %s', url)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise ValueError('response.status_code: {}'.format(response.status_code))

    jsonObj = json.loads(response.text)
    return jsonObj['content']


def save_file(category, id, content):
    if os.path.exists('data/{}/'.format(category)) == False:
        os.mkdir('data/{}/'.format(category))
    with open('data/{}/{}.html'.format(category, id), 'w') as f:
        f.write(content)


category = 'developer-blog'
post_ids = get_posts(category)
for post_id in post_ids:
    logging.info('post_id: %d', post_id)
    content = get_post(post_id)
    save_file(category, post_id, content)
