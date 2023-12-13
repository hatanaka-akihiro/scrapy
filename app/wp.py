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


def get_posts(file):
    number = 100
    url = 'https://public-api.wordpress.com/rest/{}/sites/{}/posts/?order=ASC&order_by=ID&fields=ID,URL,slug&status=publish&number={}'.format(
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


def get_post(slug):
    url = 'https://public-api.wordpress.com/rest/{}/sites/{}/posts/slug:{}'.format(
        API_VERSION, DOMAIN, slug
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


list_path = './urls.txt'
with open(list_path, 'w') as file:
    get_posts(file)

#for slug in slugs:
#    logging.info('slug: %s', slug)
#    content = get_post(slug)
#    save_file(category, slug, content)
