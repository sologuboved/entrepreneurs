# -*- coding: utf-8 -*-

from json_operations import *

NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'

PE_NAMES_44 = 'pe_names_44.json'
PE_NAMES_F = 'pe_names_f.json'
PE_NAMES_M = 'pe_names_m.json'
PE_UNCLEAR = 'pe_unclear.json'

FINAL_MERGED_CONTACT_NAMES = 'final_merged_contact_names.json'
CONTACT_NAMES_F = 'contact_names_f.json'
CONTACT_NAMES_M = 'contact_names_m.json'
CONTACT_UNCLEAR = 'contact_unclear.json'


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


def launch(source_json_file, namebase_f_file, namebase_m_file, names_f_file, names_m_file, unclear_file):
    raw_names = load_json(source_json_file)
    cleaned_names = clean_names(raw_names)
    dump_json(cleaned_names, source_json_file)
    group_names(source_json_file, namebase_f_file, namebase_m_file, names_f_file, names_m_file, unclear_file)


if __name__ == '__main__':
    launch(FINAL_MERGED_CONTACT_NAMES,
           NAMEBASE_F, NAMEBASE_M,
           CONTACT_NAMES_F, CONTACT_NAMES_M, CONTACT_UNCLEAR)
