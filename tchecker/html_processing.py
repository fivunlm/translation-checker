import os
import re


def find_html_files(base_dir):
    html_files = []

    for dir_path, dir_names, file_names in os.walk(base_dir):
        for f in file_names:
            full_file_path = os.path.join(dir_path, f)
            if full_file_path.endswith('.html'):
                html_files.append(full_file_path)

        for d in dir_names:
            html_files += find_html_files(os.path.join(dir_path, d))

    return html_files


def find_res_keys(file_path):
    reg_ex = re.compile(r'\{res:(\w+)\}')
    keys = []
    with open(file_path, 'r') as file:
        line = file.readline()
        while line:
            keys += reg_ex.findall(line)
            line = file.readline()
    return keys


def get_all_keys_from_html(base_dir):
    keys = []
    html_files = find_html_files(base_dir)
    for f in html_files:
        print('Parsing %s' % f)
        keys += find_res_keys(f)

    return keys
