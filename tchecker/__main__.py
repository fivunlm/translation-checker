import argparse
import os
import tabulate

from .html_parser import get_all_resources_from_html
from .language_file_processing import get_all_keys_from_lang


def do_check(base_dir, lang_files, show_missing_keys):
    result_rows = []
    translatable_resources = get_all_resources_from_html(base_dir)
    result_rows.append(['html', len(translatable_resources), '-'])
    have_missing_keys = False

    for file in lang_files:
        missing_keys_count = 0
        lang_keys = set(get_all_keys_from_lang(os.path.join(base_dir, file)))

        if show_missing_keys:
            print('Missing keys for file %s' % file)
            print('---------------------------------------------------------------')

        for tr in translatable_resources:

            if tr.key not in lang_keys:
                missing_keys_count += 1
                have_missing_keys = True

                if show_missing_keys:
                    print_translation_resource(tr)

        result_rows.append([file, len(lang_keys), missing_keys_count])

    print(tabulate.tabulate(result_rows, headers=['File/s', 'Total keys', 'Missing Keys'], tablefmt='grid'))

    return -1 if have_missing_keys else 0


def print_translation_resource(tr):

        print('[%s] Found in:' % tr.key)
        for l in tr.locations:
            print('    File: %s Line: %d' % (l.file, l.line))


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


def main():
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

    ret_code = do_check(args.base_dir, language_files, args.show_keys)
    exit(ret_code)


if __name__ == '__main__':
    main()
