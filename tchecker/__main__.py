import argparse
import os

import sys
import tabulate

from .models import TranslatableResourceSet
from .file_utils import get_all_files
from .parsing_utils import get_resources_from_html_file, get_resources_from_php_file, get_all_keys_from_lang, \
    get_resources_from_cpp_file


class CheckResult:
    def __init__(self):
        self.html_file_count = 0
        self.html_key_count = 0
        self.php_file_count = 0
        self.php_key_count = 0
        self.cpp_file_count = 0
        self.cpp_key_count = 0
        self.lang_checks = []

    def add_lang_keys(self, lang_file, total_keys, missing_keys):
        self.lang_checks.append(
            {
                'lang': lang_file,
                'total_keys': total_keys,
                'missing_keys': missing_keys
            }
        )


class TranslationChecker:
    def __init__(self):
        self._resources = TranslatableResourceSet()

    def _get_resources_not_present_in_list(self, list_of_keys):
        missing_keys = TranslatableResourceSet()

        for tr in self._resources:
            if tr.key not in list_of_keys:
                missing_keys.append(tr)
        return missing_keys

    def check(self, base_dir, langs):
        check_result = CheckResult()
        html_files, php_files, cpp_files, lang_files = get_all_files(base_dir, langs)

        for html_file in html_files:
            # Go to each html file and collect translatable resources
            r_in_file = get_resources_from_html_file(html_file)
            self._resources += r_in_file

        check_result.html_file_count = len(html_files)
        check_result.html_key_count = len(self._resources)

        for php_file in php_files:
            # Go to each php file and collect translatable resources
            r_in_file = get_resources_from_php_file(php_file)
            self._resources += r_in_file

        check_result.php_file_count = len(php_files)
        check_result.php_key_count = len(self._resources) - check_result.html_key_count

        for cpp_file in cpp_files:
            # Go to each cpp file and collect translatable resources
            r_in_file = get_resources_from_cpp_file(cpp_file)
            self._resources += r_in_file

        check_result.cpp_file_count = len(cpp_files)
        check_result.cpp_key_count = len(self._resources) - check_result.html_key_count - check_result.php_key_count

        for lang_file in lang_files:
            lang_keys = get_all_keys_from_lang(lang_file)
            missing_keys = self._get_resources_not_present_in_list(lang_keys)
            check_result.add_lang_keys(lang_file, len(lang_keys), missing_keys)

        return check_result


def print_translation_resource(tr):
    print('[%s] Found in:' % tr.key)
    for l in tr.locations:
        print('    File: %s Line: %d' % (l.file, l.line))


def sanitize_lang_files(files):
    sanitized_files = []
    for f in files:
        name = name if '.txt' in f else '%s.txt' % f
        sanitized_files.append(name)
    return sanitized_files


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('base_dir', )
    argument_parser.add_argument('language_files')
    argument_parser.add_argument('--show-keys', action='store_true', default=False)

    args = argument_parser.parse_args()

    if not os.path.isdir(args.base_dir):
        print('%s is not a directory' % args.base_dir)
        exit(-1)

    language_files = sanitize_lang_files(args.language_files.split(','))
    if len(language_files) == 0:
        print('Language files not provided')
        exit(-1)

    tchecker = TranslationChecker()
    check_result = tchecker.check(args.base_dir, language_files)

    rows = [['html', check_result.html_file_count, check_result.html_key_count, '-'],
            ['php', check_result.php_file_count, check_result.php_key_count, '-'],
            ['cpp', check_result.cpp_file_count, check_result.cpp_key_count, '-']]

    for lang_result in check_result.lang_checks:
        rows.append([
            os.path.basename(lang_result['lang']),
            '-',
            lang_result['total_keys'],
            len(lang_result['missing_keys'])
        ])

    print(tabulate.tabulate(rows, headers=['File/s ', 'File Count', 'Total Keys', 'Missing Keys'], tablefmt='grid'))

    if args.show_keys:
        for result in check_result.lang_checks:
            print('Language file %s has %d missing keys' % (result['lang'], len(result['missing_keys'])))
            for tr in result['missing_keys']:
                print_translation_resource(tr)

    ret_code = -1 if len(check_result.lang_checks) > 0 else 0
    exit(ret_code)


if __name__ == '__main__':
    main()
