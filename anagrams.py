# -*- coding: utf-8 -*-

from json_operations import load_json
from correct_typos import *

NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'


def count_anagrams(namebase_filename):
    anagrams = list()
    namebase = set(load_json(namebase_filename))
    print len(namebase)
    while namebase:
        anagram = set()
        curr_name = namebase.pop()
        for name in namebase:
            if is_suitable(curr_name, name):
                anagram.add(curr_name)
                anagram.add(name)
        if anagram:
            anagrams.append(anagram)
        namebase -= anagram
    print len(anagrams)
    print
    print
    for anagram in anagrams:
        print
        for name in anagram:
            print name
        print


if __name__ == '__main__':
    print count_anagrams(NAMEBASE_M)
