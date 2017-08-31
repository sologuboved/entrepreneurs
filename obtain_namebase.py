# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

URL_F = 'http://kakzovut.ru/woman.html'
URL_M = 'http://kakzovut.ru/man.html'
NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'


def scrape_names(url):
    """
    :param url: string (url)
    :return: list
    Scrape names from page
    """
    soup = BeautifulSoup(requests.get(url).content)
    return [name.find_all('a')[0].text for name in soup.find_all('div', {'class': 'nameslist'})]


def amplify_namebase(names, fem=False):
    """
    :param names: list
    :param fem: True or False
    :return: list
    Include Фекла in addition to Фёкла, etc.
    Add names that are popular but missing from the original namebase
    """

    amplified = list()

    for name in names:
        amplified.append(name)
        if u'ё' in name:
            amplified.append(substitute_ye_for_yo(name))

    if fem:
        amplified.extend([u'Наталия', u'София'])

    else:
        amplified.extend([u'Ринат',  u'Магомед',  u'Ильдар',  u'Данил',  u'Аслан',  u'Рустем',  u'Ренат',  u'Ришат',
                          u'Афанасий',  u'Гагик'])

    return amplified


def substitute_ye_for_yo(name):
    """
    :param name: string
    :return: string
    Substitute ё for е in the given name
    """
    substituted = ''
    for char in name:
        if char == u'ё':
            substituted += u'е'
        else:
            substituted += char
    return substituted


if __name__ == '__main__':
    # names_f = scrape_names(URL_F)
    # dump_json(names_f, NAMEBASE_F)
    #
    # names_m = scrape_names(URL_M)
    # dump_json(names_m, NAMEBASE_M)

    # dump_json(amplify_namebase(load_json(NAMEBASE_F), fem=True), NAMEBASE_F)
    # dump_json(amplify_namebase(load_json(NAMEBASE_M)), NAMEBASE_M)

    pass

