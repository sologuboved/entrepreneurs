# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from json_operations import *

URL_F = 'http://kakzovut.ru/woman.html'
URL_M = 'http://kakzovut.ru/man.html'
NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'
ADDITIONAL_F = 'additional_f.txt'
ADDITIONAL_M = 'additional_m.txt'


def scrape_names(url):
    """
    :param url: string (url)
    :return: list
    Scrape names from page
    """
    print "Scraping names..."
    soup = BeautifulSoup(requests.get(url).content)
    names = [name.find_all('a')[0].text for name in soup.find_all('div', {'class': 'nameslist'})]
    without_brackets = list()
    for name in names:
        variants = name.split()
        without_brackets.append(variants[0])
        try:
            without_brackets.append(variants[1][1: -1])
        except IndexError:
            pass
    return without_brackets


def amplify_namebase(names, additional):
    """
    :param names: list
    :param additional: str (filename)
    :return: list
    Include Фекла in addition to Фёкла, etc.
    Add names that are popular but missing from the original namebase
    """

    print "Amplifying namebase..."

    amplified = list()

    for name in names:
        amplified.append(name)
        if u'ё' in name:
            amplified.append(substitute_ye_for_yo(name))

    with open(additional) as handler:
        for name in handler.readlines():
            amplified.append(name.strip())

    return amplified


def substitute_ye_for_yo(name):
    """
    :param name: string
    :return: string
    Substitute ё for е in the given name
    """
    print u"Substituting е for ё..."
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
    #
    # dump_json(amplify_namebase(load_json(NAMEBASE_F), ADDITIONAL_F), NAMEBASE_F)
    # dump_json(amplify_namebase(load_json(NAMEBASE_M), ADDITIONAL_M), NAMEBASE_M)

    for n in load_json(NAMEBASE_M):
        print n
