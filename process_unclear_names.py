# -*- coding: utf-8 -*-

from process_names import load_json, dump_json

NAMEBASE_F = 'namebase_f.json'
NAMEBASE_M = 'namebase_m.json'

PE_UNCLEAR = 'pe_unclear.json'
CONTACT_UNCLEAR = 'contact_unclear.json'
PROCESSED_PE_UNCLEAR = 'processed_pe_unclear.json'
PROCESSED_CONTACT_UNCLEAR = 'processed_contact_unclear.json'


def eliminate_abbr(source_unclear, processed_unclear):
    dump_json([name for name in load_json(source_unclear) if len(name) > 2], processed_unclear)


def eliminate_patronyms(source_unclear, processed_unclear):
    names = list()
    for name in load_json(source_unclear):
        if name[-2:] != u'ич' and name[-3:] != u'вна' and name[-3:] != u'чна' and name[-3:] != u'шна':
            names.append(name)
    dump_json(names, processed_unclear)


def eliminate_declension(source_unclear, processed_unclear, namebase_f, namebase_m):
    to_add_f = list()
    to_add_m = list()
    still_unclear = list()
    namebase_f = load_json(namebase_f)
    namebase_m = load_json(namebase_m)

    for name in load_json(source_unclear):
        nominative = get_nominative(name)
        if nominative in namebase_f:
            to_add_f.append(nominative)
        elif nominative in namebase_m:
            to_add_m.append(nominative)
        else:
            still_unclear.append(name)

    print 'F:', len(to_add_f)
    for name in set(to_add_f):
        print name
    print
    print 'M:', len(to_add_m)
    for name in set(to_add_m):
        print name
    print
    print 'U:', len(still_unclear)


def get_nominative(name):
    inflections = {u'ы': u'а', u'и': u'я', u'а': u'', u'я': u'й'}
    try:
        return name[: -1] + inflections[name[-1]]
    except KeyError:
        return


if __name__ == '__main__':
    # eliminate_patronyms(CONTACT_UNCLEAR, PROCESSED_CONTACT_UNCLEAR)
    # eliminate_abbr(PROCESSED_CONTACT_UNCLEAR, PROCESSED_CONTACT_UNCLEAR)
    eliminate_declension(PROCESSED_CONTACT_UNCLEAR, PROCESSED_CONTACT_UNCLEAR, NAMEBASE_F, NAMEBASE_M)
    pass
