# -*- coding: utf-8 -*-

import json

NAMES_JSON = 'names_44.json'


def load_json(json_file):
    with open(json_file) as data:
        return json.load(data)


def compile_freq_dict(names):
    freq_dict = dict()
    for name in names:
        freq_dict[name.lower()] = freq_dict.get(name.lower(), 0) + 1
    return freq_dict


def sort_freq_dict(freq_dict):
    names = freq_dict.items()
    return sorted(names, key=lambda n: n[1], reverse=True)

if __name__ == '__main__':
    all_names = load_json(NAMES_JSON).values()
    first20 = sort_freq_dict(compile_freq_dict(all_names[:]))
    for each_name, freq in first20:
        print each_name, freq

