# Translation Check Tool

    usage: tchecker [-h] [--show-keys] base_dir language_files

It looks all translation keys (akka {res:some_key}) on all html contained on *base_dir* and its subdirectories. Then it parses all keys contained on the *language file/s*.
After done that it looks for all keys existing on translation files not present on each language file.

It shows the result of the analysis as this:

    +----------+--------------+----------------+
    | File/s   |   Total keys | Missing Keys   |
    +==========+==============+================+
    | html     |         1372 | -              |
    +----------+--------------+----------------+
    | en.txt   |         4565 | 32             |
    +----------+--------------+----------------+

By passing *--show-keys* argument it will print a list of missing keys for each language file if any.

Ir returns 0 if no key is missing, -1 otherwise.

## Example of usage ##

    tchecker C:\HtmlFiles\ en,es
    ........
    Missing keys for file pt.txt
    ---------------------------------------------------------------
    date_last_sent_attempt
    .........
    +----------+--------------+----------------+
    | File/s   |   Total keys | Missing Keys   |
    +==========+==============+================+
    | html     |         1372 | -              |
    +----------+--------------+----------------+
    | en.txt   |         4565 | 32             |
    +----------+--------------+----------------+
    | es.txt   |         4540 | 36             |
    +----------+--------------+----------------+


