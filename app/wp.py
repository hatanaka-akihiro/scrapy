import requests
import json
import logging

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, handlers=[stream_handler])

# API_TOKEN = os.environ.get('API_TOKEN')
API_TOKEN = "!%7Mp21L4BI7mk4k@k@DzhiqV8HWUtS$9lFb4GRZ)WxQ&*uylLPyusq!kki$OWaz"

API_VERSION = 'v1.1'
DOMAIN = 'support.questetra.com'

HEADERS = {'Authorization': 'Bearer {}'.format(API_TOKEN)}

def get_posts(category):
    number = 3
    url = 'https://public-api.wordpress.com/rest/{}/sites/{}/posts/?number={}&order_by=ID&fields=ID&status=publish&category={}'.format(
        API_VERSION, DOMAIN, number, category
    )
    logging.info('url: %s', url)
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise ValueError('response.status_code: {}'.format(response.status_code))

    jsonObj = json.loads(response.text)
    logging.info('found: %d, posts.length: %d', jsonObj['found'], len(jsonObj['posts']))
    return jsonObj['posts']

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

posts = get_posts('developer-blog')
for post in posts:
    content = get_post(post['ID'])
    logging.info('%d: %s', post['ID'], content)