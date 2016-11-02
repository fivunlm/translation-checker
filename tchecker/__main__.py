import argparse
import os
import tabulate

from .html_processing import get_all_keys_from_html
from .language_file_processing import get_all_keys_from_lang


def main(base_dir, lang_files, show_missing_keys):
    rows = []
    html_keys = set(get_all_keys_from_html(base_dir))
    rows.append(['html', len(html_keys), '-'])
    have_missing_keys = False

    for file in lang_files:
        counter = 0
        lang_keys = set(get_all_keys_from_lang(os.path.join(base_dir, file)))

        if show_missing_keys:
            print('Missing keys for file %s' % file)
            print('---------------------------------------------------------------')

        for html_key in html_keys:
            if html_key not in lang_keys:
                counter += 1
                have_missing_keys = True
                if show_missing_keys:
                    print(html_key)
        rows.append([file, len(lang_keys), counter])

    print(tabulate.tabulate(rows, headers=['File/s', 'Total keys', 'Missing Keys'], tablefmt='grid'))
    return -1 if have_missing_keys else 0


def check_lang_files(base_directory, files):
    checked_files = []
    for f in files:
        name = name if '.ini' in f else '%s.txt' % f
        full_path = os.path.join(base_directory, name)
        if os.path.isfile(full_path):
            checked_files.append(name)
        else:
            print('File %s not found in dir %s' % (name, base_directory))

    return checked_files


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('base_dir', )
    argument_parser.add_argument('language_files')
    argument_parser.add_argument('--show-keys', action='store_true', default=False)

    args = argument_parser.parse_args()

    if not os.path.isdir(args.base_dir):
        print('%s is not a directory' % args.base_dir)
        exit(-1)

    language_files = check_lang_files(args.base_dir, args.language_files.split(','))
    if len(language_files) == 0:
        print('Language files not provided')
        exit(-1)

    ret_code = main(args.base_dir, language_files, args.show_keys)
    exit(ret_code)
