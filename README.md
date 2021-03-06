# Translation Check Tool

    usage: tchecker [-h] [--show-keys] base_dir language_files

It looks all translation keys on all html, php and cpp/h files contained on *base_dir* and its subdirectories. Then it parses all keys contained on the *language file/s*.
After done that it looks for all keys existing on html files not present on each language file.

## Translation Keys
The definition of translations keys varies according file kind:

* For HTML:  `{res:some_key}`
* For PHP:   `$CCSLocales->GetText("some_key")`
* For CPP/H: `SSF_TRANS_SOME_KEY`

# Output

It shows the result of the analysis as this:

    +-----------+--------------+--------------+----------------+
    | File/s    | File Count   |   Total Keys | Missing Keys   |
    +===========+==============+==============+================+
    | html      | 1254         |         1370 | -              |
    +-----------+--------------+--------------+----------------+
    | php       | 831          |          571 | -              |
    +-----------+--------------+--------------+----------------+
    | cpp       | 5574         |         2024 | -              |
    +-----------+--------------+--------------+----------------+
    | en.txt    | -            |         4570 | 532            |
    +-----------+--------------+--------------+----------------+


By passing *--show-keys* argument it will print a list of missing keys for each language file with detailed info  if any.

Ir returns 0 if no key is missing, -1 otherwise.

## Example of usage ##

    tchecker C:\HtmlFiles\ en,es --show-keys
    ........
    Missing keys for file en.txt
    ---------------------------------------------------------------
    [lm_profile_id] Found in:
        File: C:\HtmlFiles\ProfList.html Line: 66
    [count] Found in:
        File: C:\HtmlFiles\Attendant.html Line: 138
        File: C:\HtmlFiles\Consolidated.html Line: 218
    [customers_tags] Found in:
        File: C:\HtmlFiles\CustomersTag.html Line: 73
        File: C:\HtmlFiles\CustomersTag.html Line: 119
        File: C:\HtmlFiles\CustomersTag.html Line: 188

# Installation #
1. Clone this repo or download (and decompress) the zip file
2. Change directory to translation-checker
3. Execute the command ``pip install .``

## Requirements ##
* Python 3
* Pip



