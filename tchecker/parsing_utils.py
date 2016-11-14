import re

from tchecker.models import TranslatableResource, TranslatableResourceSet


def _get_resources_for_file_and_regex(reg_ex_str, file_path):
    reg_ex = re.compile(reg_ex_str)
    resources = TranslatableResourceSet()

    try:
        with open(file_path, 'r', encoding="utf8") as file:
            line = file.readline()
            line_number = 1

            while line:
                for key in reg_ex.findall(line):
                    tr = TranslatableResource(key)
                    tr.add_location(file_path, line_number)
                    resources.append(tr)

                line = file.readline()
                line_number += 1
    except Exception as ex:
        pass

    return resources


def get_resources_from_html_file(file_path):
    return _get_resources_for_file_and_regex(r'\{res:(\w+)\}', file_path)


def get_resources_from_php_file(file_path):
    return _get_resources_for_file_and_regex(r'\$CCSLocales->GetText\(\"(\w+)\"\)', file_path)


def get_resources_from_cpp_file(file_path):
    return _get_resources_for_file_and_regex(r'(SSF_TRANS\w+)', file_path)


def get_all_keys_from_lang(file_path):
    reg_ex = re.compile(r'^(\w+)=.+')
    keys = []
    with open(file_path, 'r', encoding="utf8") as file:
        line = file.readline()
        while line:
            keys += reg_ex.findall(line)
            line = file.readline()
    return keys