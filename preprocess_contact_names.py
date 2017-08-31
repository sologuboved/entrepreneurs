# -*- coding: utf-8 -*-

from json_operations import *

CONTACT_NAMES_2014 = 'contact_names_2014.json'
CONTACT_NAMES_2015 = 'contact_names_2015.json'
CONTACT_NAMES_2016 = 'contact_names_2016.json'
CONTACT_NAMES_2017 = 'contact_names_2017.json'
ED_CONTACT_NAMES_2014 = 'ed_contact_names_2014.json'
ED_CONTACT_NAMES_2015 = 'ed_contact_names_2015.json'
ED_CONTACT_NAMES_2016 = 'ed_contact_names_2016.json'
ED_CONTACT_NAMES_2017 = 'ed_contact_names_2017.json'
FINAL_CONTACT_NAMES_2014 = 'final_contact_names_2014.json'
FINAL_CONTACT_NAMES_2015 = 'final_contact_names_2015.json'
FINAL_CONTACT_NAMES_2016 = 'final_contact_names_2016.json'
FINAL_CONTACT_NAMES_2017 = 'final_contact_names_2017.json'
MERGED_CONTACT_NAMES = 'merged_contact_names.json'
ED_MERGED_CONTACT_NAMES = 'ed_merged_contact_names.json'
FINAL_MERGED_CONTACT_NAMES = 'final_merged_contact_names.json'
TEST_JSON_0 = 'test0.json'
TEST_JSON_1 = 'test1.json'


def eliminate_repeating_lines(json_file, ed_json_file):
    print "Starting load..."
    all_lines = load_json(json_file)
    to_keep = list()
    num_repetitions = 0
    previous_line = None
    print "Starting search..."
    for line in all_lines:
        if line == previous_line:
            num_repetitions += 1
            print num_repetitions, 'repetitions'
        else:
            to_keep.append(line)
            previous_line = line
    print "Starting dump..."
    dump_json(to_keep, ed_json_file)
    print len(all_lines)


def print_remaining_duplicates(json_file):
    all_lines = load_json(json_file)
    already_there = set()
    for (x, y, z) in all_lines:
        if (x, y, z) not in already_there:
            already_there.add((x, y, z))
        else:
            print x, y, z


def eliminate_remaining_duplicates(json_file, final_json_file):
    all_lines = [(x, y, z) for x, y, z in load_json(json_file)]
    without_duplicates = set(all_lines)
    print len(all_lines) - len(without_duplicates), "apparent duplicates"
    print len(without_duplicates), "lines remain"
    without_duplicates = [[x, y, z] for x, y, z in without_duplicates]
    print "Starting dump..."
    dump_json(without_duplicates, final_json_file)


def merge_contact_names(merged_json_file, *args):
    merged_contact_names = list()
    for fileling in args:
        print 'Loading', fileling + '...'
        names = load_json(fileling)
        merged_contact_names.extend(names)
    print "Dumping merged json..."
    dump_json(merged_contact_names, merged_json_file)
    check = load_json(merged_json_file)
    print len(check)


def elicit_first_names(json_file, final_json_file):
    dump_json([name[0] for name in load_json(json_file)], final_json_file)


if __name__ == '__main__':
    # list_of_lines = [['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c'], ['a', 'b', 'c'],
    #                  ['x', 'y', 'z'],
    #                  ['h', 'i', 'j'], ['h', 'i', 'j'],
    #                  ['k', 'l', 'm'],
    #                  ['n', 'o', 'p'], ['n', 'o', 'p'], ['n', 'o', 'p'], ['n', 'o', 'p'], ['n', 'o', 'p'],
    #                  ['a', 'b', 'c'],
    #                  ['n', 'o', 'p'],
    #                  ['x', 'y', 'z'], ['x', 'y', 'z'], ['x', 'y', 'z'],
    #                  ['k', 'l', 'm'], ['k', 'l', 'm'],
    #                  ['h', 'i', 'j'],
    #                  ['a', 'b', 'c'],
    #                  ['k', 'l', 'm'],
    #                  ['x', 'y', 'z'], ['x', 'y', 'z']]
    # dump_json(list_of_lines, TEST_JSON_0)
    # find_repeating_lines(TEST_JSON_0, TEST_JSON_1)
    # eliminate_repeating_lines(CONTACT_NAMES_2014, ED_CONTACT_NAMES_2014)
    # eliminate_repeating_lines(CONTACT_NAMES_2015, ED_CONTACT_NAMES_2015)
    # eliminate_repeating_lines(CONTACT_NAMES_2016, ED_CONTACT_NAMES_2016)
    # eliminate_repeating_lines(CONTACT_NAMES_2017, ED_CONTACT_NAMES_2017)
    # print_remaining_duplicates(ED_CONTACT_NAMES_2017)
    # eliminate_remaining_duplicates(ED_CONTACT_NAMES_2017, FINAL_CONTACT_NAMES_2017)
    # merge_contact_names(MERGED_CONTACT_NAMES,
    #                     FINAL_CONTACT_NAMES_2014,
    #                     FINAL_CONTACT_NAMES_2015,
    #                     FINAL_CONTACT_NAMES_2016,
    #                     FINAL_CONTACT_NAMES_2017)
    # eliminate_remaining_duplicates(MERGED_CONTACT_NAMES, ED_MERGED_CONTACT_NAMES)
    elicit_first_names(ED_MERGED_CONTACT_NAMES, FINAL_MERGED_CONTACT_NAMES)

    pass
