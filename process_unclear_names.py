# -*- coding: utf-8 -*-

from json_operations import *
from correct_typos import is_suitable

NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'

PROCESSED_PE_UNCLEAR = 'processed_pe_unclear.json'
PROCESSED_CONTACT_UNCLEAR = 'processed_contact_unclear.json'

PE_NAMES_F = 'pe_names_f.json'
PE_NAMES_M = 'pe_names_m.json'
PE_UNCLEAR = 'pe_unclear.json'
CONTACT_NAMES_F = 'contact_names_f.json'
CONTACT_NAMES_M = 'contact_names_m.json'
CONTACT_UNCLEAR = 'contact_unclear.json'


class Unclear(object):
    def __init__(self, namebase_f, namebase_m, names_f_f, names_m_f, unclear_f, processed_unclear_f):
        self.namebase_f = namebase_f
        self.namebase_m = namebase_m
        self.names_f_f = names_f_f
        self.names_m_f = names_m_f
        self.processed_unclear_f = processed_unclear_f
        self.still_unclear = load_json(unclear_f)
        self.to_add_f = list()
        self.to_add_m = list()
        self.initial_total = len(self.still_unclear)
        self.eliminations_count = 0

    @staticmethod
    def get_nominative(name):
        inflections = {u'ы': u'а', u'и': u'я', u'а': u'', u'я': u'й'}  # no Игорь
        try:
            return name[: -1] + inflections[name[-1]]
        except KeyError:
            return

    @staticmethod
    def check_name_for_typo(uncl_name, name_count, total, namebase):

        def print_typo_correction():
            print name_count, "out of", total
            print uncl_name,
            print " --> ",
            print orig_name
            print

        for orig_name in namebase:
            if orig_name[0].lower() == uncl_name[0].lower():
                if is_suitable(orig_name, uncl_name):
                    print_typo_correction()
                    return orig_name

        for orig_name in namebase:
            if is_suitable(orig_name, uncl_name):
                print_typo_correction()
                return orig_name

    def print_additional_names(self, female=True, male=True):
        if female:
            print "Newly found female names:", len(self.to_add_f), 'names'
            for name in sorted(list(set(self.to_add_f))):
                print name
            print
        if male:
            print "Newly found male names:", len(self.to_add_m), 'names'
            for name in sorted(list(set(self.to_add_m))):
                print name
            print

    def print_current_unclear(self, no_rep=True, lim=False):
        print "Still unclear:", len(self.still_unclear), 'names'
        if no_rep:
            current_unclear = sorted(list(set(self.still_unclear)))
        else:
            self.still_unclear.sort()
            current_unclear = self.still_unclear
        if not lim:
            lim = float('inf')
        index = 0
        while index < lim and index < len(current_unclear):
            print current_unclear[index]
            index += 1
        print

    def print_resume(self):
        print curr_unclear.eliminations_count, "out of", curr_unclear.initial_total, 'eliminated'
        print "%d f names and %d m names are to be added" % (len(self.to_add_f), len(self.to_add_m))
        print
        print

    def extract_first_names(self):
        print "Extracting first names..."

        namebase_f = load_json(self.namebase_f)
        namebase_m = load_json(self.namebase_m)
        without_postfixes = list()
        count_f = count_m = 0

        for name in self.still_unclear:
            name = name.split()[0]

            if name in namebase_f:
                self.to_add_f.append(name)
                count_f += 1

            elif name in namebase_m:
                self.to_add_m.append(name)
                count_m += 1

            else:
                without_postfixes.append(name)

        previous_l = len(self.still_unclear)
        curr_l = len(without_postfixes)
        print "Out of %d names %d are left; %d f names and %d m names added" % (previous_l, curr_l, count_f, count_m)
        self.still_unclear = without_postfixes
        self.eliminations_count += (previous_l - curr_l)
        print

    def eliminate_nonalpha(self):
        print "Eliminating nonalpha..."

        count = 0
        without_nonalphas = list()

        for name in self.still_unclear:

            if not name.isalpha():
                alphaed_name = str()
                for char in name:
                    if char.isalpha():
                        alphaed_name += char
                    else:
                        count += 1
                if alphaed_name:
                    without_nonalphas.append(alphaed_name)

            else:
                without_nonalphas.append(name)

        prev_l = len(self.still_unclear)
        curr_l = len(without_nonalphas)
        diff = prev_l - curr_l
        print "Out of %d names %d are left; %d nonaplha strings and %d nonalpha characters eliminated" \
              % (prev_l, curr_l, diff, count)
        self.still_unclear = without_nonalphas
        self.eliminations_count += diff
        print

    def eliminate_abbr(self):
        print "Eliminating abbreviations..."
        prev_l = len(self.still_unclear)
        self.still_unclear = [name for name in self.still_unclear if len(name) > 2]
        curr_l = len(self.still_unclear)
        diff = prev_l - curr_l
        print "Out of %d names %d are left; %d abbreviations eliminated" % (prev_l, curr_l, diff)
        self.eliminations_count += diff
        print

    def eliminate_patronyms(self):
        print "Eliminating patronyms..."
        without_patronyms = list()
        for name in self.still_unclear:
            if name[-2:] != u'ич' and name[-3:] != u'вна' and name[-3:] != u'чна' and name[-3:] != u'шна':
                without_patronyms.append(name)

        prev_l = len(self.still_unclear)
        curr_l = len(without_patronyms)
        diff = prev_l - curr_l
        print "Out of %d names %d are left; %d patronyms eliminated" % (prev_l, curr_l, diff)

        self.still_unclear = without_patronyms
        self.eliminations_count += diff
        print

    def eliminate_declension(self, show=False):
        print "Eliminating declension..."
        count_f = count_m = 0
        namebase_f = load_json(self.namebase_f)
        namebase_m = load_json(self.namebase_m)
        without_declension = list()

        for name in self.still_unclear:
            print '* ',
            nominative = self.get_nominative(name)
            if nominative in namebase_f:
                self.to_add_f.append(nominative)
                count_f += 1
            elif nominative in namebase_m:
                self.to_add_m.append(nominative)
                count_m += 1
            else:
                without_declension.append(name)

        print
        prev_l = len(self.still_unclear)
        curr_l = len(without_declension)
        print "Out of %d names %d are left; %d f names and %d m names added" % (prev_l, curr_l, count_f, count_m)
        self.still_unclear = without_declension
        self.eliminations_count += (prev_l - curr_l)
        print

    def eliminate_typos(self):
        print "Eliminating typos..."
        name_count = count_f = count_m = 0
        namebase_f = load_json(self.namebase_f)
        namebase_m = load_json(self.namebase_m)
        without_typos = list()
        total = len(self.still_unclear)

        for uncl_name in self.still_unclear:
            name_count += 1

            if uncl_name == u'Имя' or uncl_name == u'имя':
                without_typos.append(uncl_name)
                continue

            good_f_name = self.check_name_for_typo(uncl_name, name_count, total, namebase_f)
            if good_f_name:
                count_f += 1
                self.to_add_f.append(good_f_name)
                continue

            good_m_name = self.check_name_for_typo(uncl_name, name_count, total, namebase_m)
            if good_m_name:
                count_m += 1
                self.to_add_m.append(good_m_name)
                continue

            without_typos.append(uncl_name)

        prev_l = len(self.still_unclear)
        curr_l = len(without_typos)
        print "Out of %d names %d are left; %d f names and %d m names added" % (prev_l, curr_l, count_f, count_m)
        self.still_unclear = without_typos
        self.eliminations_count += (prev_l - curr_l)
        print

    def dump_additional_names(self):
        print "Dumping female names..."
        dump_json(load_json(self.names_f_f) + self.to_add_f, self.names_f_f)
        print "Dumping male names..."
        dump_json(load_json(self.names_m_f) + self.to_add_m, self.names_m_f)
        print "Dumping unclear names..."
        dump_json(self.still_unclear, self.processed_unclear_f)


def check_coding(dubious, cyrillic):
    for index in range(len(dubious)):
        if dubious[index] != cyrillic[index]:
            print dubious[index]
            break
    else:
        print "Quite Cyrillic"


if __name__ == '__main__':
    curr_unclear = Unclear(NAMEBASE_F, NAMEBASE_M,
                           CONTACT_NAMES_F, CONTACT_NAMES_M, CONTACT_UNCLEAR,
                           PROCESSED_CONTACT_UNCLEAR)
    curr_unclear.extract_first_names()
    curr_unclear.eliminate_abbr()
    curr_unclear.eliminate_nonalpha()
    curr_unclear.eliminate_patronyms()
    curr_unclear.eliminate_declension()
    curr_unclear.eliminate_typos()
    curr_unclear.print_resume()

    curr_unclear.print_additional_names()
    curr_unclear.print_current_unclear()
    # curr_unclear.dump_additional_names()

    # TODO replacements
    # TODO capitalization
    # TODO reload f and m files
    # TODO exclude names starting with the same letter
