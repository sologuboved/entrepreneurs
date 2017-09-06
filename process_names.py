# -*- coding: utf-8 -*-

from global_vars import *
from json_operations import *
from stats import group_names

NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'
PE_NAMES_44 = 'pe_names_44.json'
FINAL_MERGED_CONTACT_NAMES = 'final_merged_contact_names.json'


def clean_names(names):
    """
    :param names: list
    :return: list
    Correct char case
    """
    print "Cleaning names..."
    return [name[0].upper() + name[1:].lower() for name in names]


def dump_grouped_names(names_file, namebase_f_file, namebase_m_file, names_f_file, names_m_file, unclear_file):
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
    print "Grouping names..."
    names_f, names_m, unclear = group_names(load_json(names_file),
                                            load_json(namebase_f_file),
                                            load_json(namebase_m_file))

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
    dump_grouped_names(source_json_file, namebase_f_file, namebase_m_file, names_f_file, names_m_file, unclear_file)


if __name__ == '__main__':
    launch(FINAL_MERGED_CONTACT_NAMES,
           NAMEBASE_F, NAMEBASE_M,
           OLD_CONTACT_NAMES_F, OLD_CONTACT_NAMES_M, OLD_CONTACT_UNCLEAR)
