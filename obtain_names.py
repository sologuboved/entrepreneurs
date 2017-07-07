# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

URL_F = 'http://kakzovut.ru/woman.html'
URL_M = 'http://kakzovut.ru/man.html'
JSON_F = 'names_f.json'
JSON_M = 'names_m.json'


def scrape_names(url):
    soup = BeautifulSoup(requests.get(url).content)
    return [name.find_all('a')[0].text for name in soup.find_all('div', {'class': 'nameslist'})]


def names_to_json(names, json_file):
    with open(json_file, 'w') as handler:
        json.dump(names, handler)


# def load_json(json_file):
#     with open(json_file) as data:
#         return json.load(data)


if __name__ == '__main__':
    names_f = scrape_names(URL_F)
    names_to_json(names_f, JSON_F)

    names_m = scrape_names(URL_M)
    names_to_json(names_m, JSON_M)

