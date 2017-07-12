# -*- coding: utf-8 -*-

from process_pe_names import *

NAMES_2014 = 'contact_names_2014.json'
NAMES_2015 = 'contact_names_2015.json'
NAMES_2016 = 'contact_names_2016.json'
NAMES_2017 = 'contact_names_2017.json'
ED_NAMES_2014 = 'ed_contact_names_2014.json'
ED_NAMES_2015 = 'ed_contact_names_2015.json'
ED_NAMES_2016 = 'ed_contact_names_2016.json'
ED_NAMES_2017 = 'ed_contact_names_2017.json'
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
    # eliminate_repeating_lines(NAMES_2014, ED_NAMES_2014)
    # eliminate_repeating_lines(NAMES_2015, ED_NAMES_2015)
    # eliminate_repeating_lines(NAMES_2016, ED_NAMES_2016)
    # eliminate_repeating_lines(NAMES_2017, ED_NAMES_2017)
    pass
