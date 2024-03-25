# `clean-text` 

User-generated content on the Web and in social media is often dirty. Preprocess your scraped data with `clean-text` to create a normalized text representation. For instance, turn this corrupted input:

```txt
A bunch of \\u2018new\\u2019 references, including [Moana](https://en.wikipedia.org/wiki/Moana_%282016_film%29).


»Yóù àré     rïght &lt;3!«
```

into this clean output:

```txt
A bunch of 'new' references, including [moana](<URL>).

"you are right <3!"
```

`clean-text` uses [ftfy](https://github.com/LuminosoInsight/python-ftfy), [unidecode](https://github.com/takluyver/Unidecode) and numerous hand-crafted rules, i.e., RegEx.

## Usage

```python
from cleantext import clean

clean("some input",
    fix_unicode=True,               # fix various unicode errors
    to_ascii=True,                  # transliterate to closest ASCII representation
    lower=True,                     # lowercase text
    no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
    no_urls=False,                  # replace all URLs with a special token
    no_emails=False,                # replace all email addresses with a special token
    no_phone_numbers=False,         # replace all phone numbers with a special token
    no_numbers=False,               # replace all numbers with a special token
    no_digits=False,                # replace all digits with a special token
    no_currency_symbols=False,      # replace all currency symbols with a special token
    no_punct=False,                 # remove punctuations
    replace_with_punct="",          # instead of removing punctuations you may replace them
    replace_with_url="<URL>",
    replace_with_email="<EMAIL>",
    replace_with_phone_number="<PHONE>",
    replace_with_number="<NUMBER>",
    replace_with_digit="0",
    replace_with_currency_symbol="<CUR>",
    lang="en"                       # set to 'de' for German special handling
)
```

Carefully choose the arguments that fit your task. The default parameters are listed above.

You may also only use specific functions for cleaning. For this, take a look at the [source code](https://github.com/jfilter/clean-text/blob/main/cleantext/clean.py).
