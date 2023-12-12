import requests
import json
import logging
import os

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, handlers=[stream_handler])

# API_TOKEN = os.environ.get('API_TOKEN')
API_TOKEN = "!%7Mp21L4BI7mk4k@k@DzhiqV8HWUtS$9lFb4GRZ)WxQ&*uylLPyusq!kki$OWaz"

API_VERSION = 'v1.1'
DOMAIN = 'support.questetra.com'

HEADERS = {'Authorization': 'Bearer {}'.format(API_TOKEN)}


def get_posts(category):
    post_ids = []
    number = 3
    url = 'https://public-api.wordpress.com/rest/{}/sites/{}/posts/?number={}&order_by=ID&fields=ID&status=publish&category={}'.format(
        API_VERSION, DOMAIN, number, category
    )
    logging.info('url: %s', url)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise ValueError('response.status_code: {}'.format(response.status_code))

    jsonObj = json.loads(response.text)
    posts = jsonObj['posts']
    logging.info('found: %d, posts.length: %d', jsonObj['found'], len(posts))
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
