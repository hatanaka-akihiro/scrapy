import os
import requests
import json

const API_TOKEN = os.environ.get('API_TOKEN')

const API_VERSION = 'v1.1'
const domain = 'support.questetra.com'
const category = 'developer-blog'
const number = 10

const url = `https://public-api.wordpress.com/rest/${API_VERSION}/sites/${encodeURIComponent(domain)}/posts/?number=${number}&order_by=ID&fields=ID&status=publish&category=${category}`;
const headers = {'Authorization':`Bearer ${API_TOKEN}`}

requests.get(url, headers=headers)

const {posts, meta} = json.loads(response.text)
const next_page = meta.next_page