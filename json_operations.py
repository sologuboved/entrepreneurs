import json


def load_json(json_file):
    with open(json_file) as data:
        return json.load(data)


def dump_json(names, json_file):
    with open(json_file, 'w') as handler:
        json.dump(names, handler)