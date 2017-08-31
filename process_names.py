# -*- coding: utf-8 -*-

from json_operations import *

NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'

PE_NAMES_44 = 'pe_names_44.json'
PE_NAMES_F = 'pe_names_f.json'
PE_NAMES_M = 'pe_names_m.json'
PE_UNCLEAR = 'pe_unclear.json'

FINAL_CONTACT_NAMES_2014 = 'final_contact_names_2014.json'
FINAL_CONTACT_NAMES_2015 = 'final_contact_names_2015.json'
FINAL_CONTACT_NAMES_2016 = 'final_contact_names_2016.json'
FINAL_CONTACT_NAMES_2017 = 'final_contact_names_2017.json'

FINAL_MERGED_CONTACT_NAMES = 'final_merged_contact_names.json'
CONTACT_NAMES_F = 'contact_names_f.json'
CONTACT_NAMES_M = 'contact_names_m.json'
CONTACT_UNCLEAR = 'contact_unclear.json'

PROCESSED_PE_UNCLEAR = 'processed_pe_unclear.json'
PROCESSED_CONTACT_UNCLEAR = 'processed_contact_unclear.json'


def clean_names(names):
    """
    :param names: list
    :return: list
    Correct char case
    """
    return [name[0].upper() + name[1:].lower() for name in names]


def group_names(names_file, namebase_f_file, namebase_m_file, names_f_file, names_m_file, unclear_file):
    """
    :param names_file: .json
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

    total_num = sum(freq_dict.values())

    for name in freq_dict:
        freq = freq_dict[name]
        freq_dict[name] = (freq, freq * 100.0 / total_num)

    return freq_dict


def sort_freq_dict(freq_dict):
    """
    :param freq_dict: dict
    :return: list of tuples
    Sort name frequencies from large to small: [(name0: max frequency), ..., (name-1: min frequency)]
    """
    return sorted(freq_dict.items(), key=lambda n: n[1], reverse=True)


def print_freqs(sorted_freqs, label, lim=None):
    """
    :param sorted_freqs: list of tuples
    :param label: string
    :param lim: int or None
    :return: None
    Prettyprint sorted name frequencies
    """
    num_names = len(sorted_freqs)
    num_entries = sum([entry[1][0] for entry in sorted_freqs])
    if not lim:
        lim = num_names
    print "FREQUENCIES OF %s NAMES" % label,
    print "[%d names, %d entries]:" % (num_names, num_entries)
    print "Printing first %d names..." % lim
    print
    index = 0
    while index < lim and index < num_names:
        name, nums = sorted_freqs[index]
        freq, percent = nums
        print name + ':', "{:.3f}".format(percent) + '%', '(' + str(freq) + ')'
        index += 1
    print
    print


def launch(source_json_file, namebase_f_file, namebase_m_file, names_f_file, names_m_file, unclear_file):
    # raw_names = load_json(source_json_file)
    # cleaned_names = clean_names(raw_names)
    # dump_json(cleaned_names, source_json_file)
    # group_names(source_json_file, namebase_f_file, namebase_m_file, names_f_file, names_m_file, unclear_file)
    print_freqs(sort_freq_dict(compile_freq_dict(load_json(names_f_file), fem=True)), 'FEMALE')
    print_freqs(sort_freq_dict(compile_freq_dict(load_json(names_m_file))), 'MALE')
    print_freqs(sort_freq_dict(compile_freq_dict(load_json(unclear_file))), 'UNCLEAR', lim=40)


if __name__ == '__main__':
    launch(FINAL_MERGED_CONTACT_NAMES,
           NAMEBASE_F, NAMEBASE_M,
           CONTACT_NAMES_F, CONTACT_NAMES_M, PROCESSED_CONTACT_UNCLEAR)
