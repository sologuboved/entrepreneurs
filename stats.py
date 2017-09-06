# -*- coding: utf-8 -*-

from json_operations import load_json
from global_vars import *


def compile_freq_dict(names):
    """
    :param names: list
    :return: dict
    Calculate name frequencies: {name: frequency}
    """
    freq_dict = dict()

    def join_variants(pair):
        first, second = pair
        if first in freq_dict and second in freq_dict:
            freq_dict[first + " / " + second] = freq_dict[first] + freq_dict[second]
            freq_dict.pop(first)
            freq_dict.pop(second)

    for name in names:
        freq_dict[name] = freq_dict.get(name, 0) + 1

    all_variants = {(u'Наталья', u'Наталия'),
                    (u'Софья', u'София'),
                    (u'Олеся', u'Алеся'),
                    (u'Нелли', u'Нелля'),
                    (u'Ахмед', u'Ахмет'),
                    (u'Даниил', u'Данил'),
                    (u'Эльдар', u'Ильдар'),
                    (u'Рустам', u'Рустем'),
                    (u'Лев', u'Лева'),
                    (u'Эдуард', u'Эдик'),
                    (u'Мурат', u'Мурад'),
                    (u'Эльдус', u'Ильдус'),
                    (u'Артем', u'Артём'),
                    (u'Федор', u'Фёдор'),
                    (u'Петр', u'Пётр'),
                    (u'Семен', u'Семён'),
                    (u'Алена', u'Алёна'),
                    (u'Фекла', u'Фёкла')
                    }
    for variants in all_variants:
        join_variants(variants)

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


def print_freqs(names, label, fem, lim=None):
    """
    :param names: list
    :param label: string
    :param fem: True, False, or None
    :param lim: int or None
    :return: None
    Prettyprint sorted name frequencies
    """
    freq_dict = compile_freq_dict(names)
    sorted_freqs = sort_freq_dict(freq_dict)
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


def group_names(names, namebase_f, namebase_m):
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

    return names_f, names_m, unclear


def launch(names_f_file, names_m_file, unclear_file):
    print_freqs(load_json(names_f_file), 'FEMALE', True)
    print_freqs(load_json(names_m_file), 'MALE', False)
    print_freqs(load_json(unclear_file), 'UNCLEAR', None, lim=40)


if __name__ == '__main__':
    launch(NEW_CONTACT_NAMES_F, NEW_CONTACT_NAMES_M, NEW_CONTACT_UNCLEAR)


