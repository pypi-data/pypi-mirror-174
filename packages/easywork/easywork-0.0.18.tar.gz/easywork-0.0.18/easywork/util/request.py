import urllib.request

import requests
from lxml import etree


def load_html(url, timeout=3):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    html = str(urllib.request.urlopen(req, timeout=timeout).read(), 'utf-8')
    return etree.HTML(html)


def ajax(cookie=None, proxies=None):
    headers = {'User-Agent': UserAgent().random}

    if cookie:
        headers['cookie'] = cookie

    if proxies:
        proxies = {
            'http': 'http://' + proxies,
            'https': 'https://' + proxies,
        }

    return headers, proxies


def get(url, timeout=3, params=None, cookie=None, proxies=None):
    headers, proxies = ajax(cookie, proxies)
    return requests.get(url, params=params, headers=headers, proxies=proxies, timeout=timeout)


def post(url, timeout=3, data=None, cookie=None, proxies=None):
    headers, proxies = ajax(cookie, proxies)
    return requests.post(url, data=data, headers=headers, proxies=proxies, timeout=timeout)
