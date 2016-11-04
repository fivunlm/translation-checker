import re


def get_all_keys_from_lang(file_path):
    reg_ex = re.compile(r'^(\w+)=.+')
    keys = []
    with open(file_path, 'r', encoding="utf8") as file:
        line = file.readline()
        while line:
            keys += reg_ex.findall(line)
            line = file.readline()
    return keys
