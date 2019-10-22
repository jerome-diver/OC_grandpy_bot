#! python3
"""
Convert JSON file verbs.json =>
    [ { VERBS } ]
        | VERBS => { Mode: { Temps: [ conjugates_verbs ] } }
to json list of unique conjugate verb's words
"""

import os
import json


DIRNAME = os.getcwd()
VERBS_JSON_FILE = os.path.join(DIRNAME, "verbs.json")
FILE_CONVERTED = "stop_verbs.json"


def remove_existing_file(f: str):
    """Remove existing converted file"""

    if os.path.exists(f):
        os.remove(f)


def convert_to_verbs_list(f: str) -> list:
    """Convert json file
    to
    list of unique verbs"""

    with open(f, "r", encoding='utf-8') as json_verbs:
        converted = set()
        verbs = json.load(json_verbs)
        for index, verb in enumerate(verbs):
            for mode in verbs[index]:
                for temps in verbs[index][mode]:
                    for idx, conjugates in enumerate(verbs[index][mode][temps]):
                        vc = verbs[index][mode][temps][idx]
                        converted.add(vc)
    return list(converted)


def create_json_file(f, verbs):
    """From list of unique verbs, create a json file"""

    with open(f, "w", encoding='utf-8') as converted_json:
        json.dump(verbs, converted_json, ensure_ascii=False)


def read_json_list(f):
    """From json file, read list content"""

    with open(f, "r") as json_file:
        verbs = json.load(json_file)
        for verb in verbs:
            print(verb)


remove_existing_file(FILE_CONVERTED)
VERBS = convert_to_verbs_list(VERBS_JSON_FILE)
create_json_file(FILE_CONVERTED, VERBS)
read_json_list(FILE_CONVERTED)
