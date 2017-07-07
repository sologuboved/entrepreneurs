# -*- coding: utf-8 -*-

import json

NAMES_44 = 'names_44.json'
NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'
NAMES_F = 'names_f.json'
NAMES_M = 'names_m.json'
UNCLEAR = 'unclear.json'


def load_json(json_file):
    with open(json_file) as data:
        return json.load(data)


def dump_json(names, json_file):
    with open(json_file, 'w') as handler:
        json.dump(names, handler)


def clean_names(names):
    """
    :param names: list
    :return: list
    Correct char case
    """
    return [name[0].upper() + name[1:].lower() for name in names]


def group_names(names_file, namebase_f_file, namebase_m_file, names_f_file, names_m_file, unclear_file):
    """
    :param names_file: .json file
    :param namebase_f_file: .json
    :param namebase_m_file: .json
    :param names_f_file: .json
    :param names_m_file: .json
    :param unclear_file: .json
    :return: None
    Classify names according to gender and dump corresponding .jsons
    """

    names = load_json(names_file)
    namebase_f = load_json(namebase_f_file)
    namebase_m = load_json(namebase_m_file)

    names_f = list()
    names_m = list()
    unclear = list()

    for name in names:
        if name in namebase_f:
            names_f.append(name)
        elif name in namebase_m:
            names_m.append(name)
        else:
            unclear.append(name)

    print "Dumping female names..."
    dump_json(names_f, names_f_file)
    print "Dumping male names..."
    dump_json(names_m, names_m_file)
    print "Dumping names of unclear gender..."
    dump_json(unclear, unclear_file)
    print
    print


def compile_freq_dict(names, fem=False):
    """
    :param names: list
    :param fem: True or False
    :return: dict
    Calculate name frequencies: {name: frequency}
    """
    freq_dict = dict()

    for name in names:
        freq_dict[name] = freq_dict.get(name, 0) + 1

    if fem:
        freq_dict[u'Наталья / Наталия'] = freq_dict[u'Наталья'] + freq_dict[u'Наталия']
        freq_dict.pop(u'Наталья', None)
        freq_dict.pop(u'Наталия', None)

        freq_dict[u'Софья / София'] = freq_dict[u'Софья'] + freq_dict[u'София']
        freq_dict.pop(u'Софья', None)
        freq_dict.pop(u'София', None)

    return freq_dict


def sort_freq_dict(freq_dict):
    """
    :param freq_dict: dict
    :return: list of tuples
    Sort name frequencies from large to small: [(name0: max frequency), ..., (name-1: min frequency)]
    """
    return sorted(freq_dict.items(), key=lambda n: n[1], reverse=True)


if __name__ == '__main__':

    # group_names(NAMES_44, NAMEBASE_F, NAMEBASE_M, NAMES_F, NAMES_M, UNCLEAR)

    print "FREQUENCIES: FEMALE",
    sorted_f = sort_freq_dict(compile_freq_dict(load_json(NAMES_F), fem=True))
    print "[%d names, %d entries]" % (len(sorted_f), sum([entry[1] for entry in sorted_f]))
    print
    for n, freq in sorted_f:
        print n + ':', freq
    print
    print

    print "FREQUENCIES: MALE",
    sorted_m = sort_freq_dict(compile_freq_dict(load_json(NAMES_M)))
    print "[%d names, %d entries]" % (len(sorted_m), sum([entry[1] for entry in sorted_m]))
    print
    for n, freq in sorted_m:
        print n + ':', freq
    print
    print

    print "FREQUENCIES: UNCLEAR",
    sorted_unclear = sort_freq_dict(compile_freq_dict(load_json(UNCLEAR)))
    print "[%d names, %d entries; showing first 20]" % (len(sorted_unclear), sum([entry[1] for entry in sorted_unclear]))
    print
    for n, freq in sorted_unclear[: 20]:
        print n + ':', freq
