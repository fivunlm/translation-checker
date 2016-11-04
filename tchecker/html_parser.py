import os
import re

from .models import TranslatableResource


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


def get_resources_from_file(file_path):
    reg_ex = re.compile(r'\{res:(\w+)\}')
    resources = []

    with open(file_path, 'r') as file:
        line = file.readline()
        line_number = 1
        while line:
            for key in reg_ex.findall(line):
                tr = TranslatableResource(key)

                if tr in resources:
                    resources[resources.index(key)].add_location(file_path, line_number)
                else:
                    tr.add_location(file_path, line_number)
                    resources.append(tr)

            line = file.readline()
            line_number += 1

    return resources


def get_all_resources_from_html(base_dir):
    resources = []
    html_files = find_html_files(base_dir)
    for f in html_files:

        for tr in get_resources_from_file(f):
            if tr in resources:
                for l in tr.locations:
                    resources[resources.index(tr.key)].add_location(l.file, l.line)
            else:
                resources.append(tr)

    return resources
