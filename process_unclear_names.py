# -*- coding: utf-8 -*-

from json_operations import load_json, dump_json

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

    @staticmethod
    def get_nominative(name):
        inflections = {u'ы': u'а', u'и': u'я', u'а': u'', u'я': u'й'}  # no Игорь
        try:
            return name[: -1] + inflections[name[-1]]
        except KeyError:
            return

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

    def eliminate_typos(self):
        print "Eliminating typos..."
        print

    def eliminate_abbr(self):
        print "Eliminating abbreviations..."
        self.still_unclear = [name for name in self.still_unclear if len(name) > 2]
        print

    def eliminate_patronyms(self):
        print "Eliminating patronyms..."
        without_patronyms = list()
        for name in self.still_unclear:
            if name[-2:] != u'ич' and name[-3:] != u'вна' and name[-3:] != u'чна' and name[-3:] != u'шна':
                without_patronyms.append(name)
        self.still_unclear = without_patronyms
        print

    def eliminate_declension(self, show=False):
        print "Eliminating declension..."
        namebase_f = load_json(self.namebase_f)
        namebase_m = load_json(self.namebase_m)
        still_unclear = list()

        for name in self.still_unclear:
            print '* ',
            nominative = self.get_nominative(name)
            if nominative in namebase_f:
                self.to_add_f.append(nominative)
            elif nominative in namebase_m:
                self.to_add_m.append(nominative)
            else:
                still_unclear.append(name)

        self.still_unclear = still_unclear
        print
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
    curr_unclear.eliminate_abbr()
    curr_unclear.eliminate_patronyms()
    curr_unclear.eliminate_declension()
    curr_unclear.print_additional_names()
    # curr_unclear.print_current_unclear()
    curr_unclear.dump_additional_names()
