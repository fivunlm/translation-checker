import os


def get_all_files(base_dir, langs):
    html_files = []
    php_files = []
    cpp_files = []
    lang_files = []

    for dir_path, dir_names, file_names in os.walk(base_dir):
        for f in file_names:
            full_file_path = os.path.join(dir_path, f)

            if full_file_path.endswith('.html'):
                html_files.append(full_file_path)
            if full_file_path.endswith('.php'):
                php_files.append(full_file_path)
            if full_file_path.endswith('.cpp') or full_file_path.endswith('.h'):
                cpp_files.append(full_file_path)
            if f in langs:
                lang_files.append(full_file_path)

        for d in dir_names:
            h, p, c, l = get_all_files(os.path.join(dir_path, d), langs)
            html_files += h
            php_files += p
            cpp_files += c
            lang_files += l

        return html_files, php_files, cpp_files, lang_files
