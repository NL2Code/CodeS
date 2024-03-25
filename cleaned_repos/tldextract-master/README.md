# tldextract 

`tldextract` accurately separates a URL's subdomain, domain, and public suffix,
using the Public Suffix List (PSL).

Say you want just the "google" part of https://www.google.com. *Everybody gets
this wrong.* Splitting on the "." and taking the 2nd-to-last element only works
for simple domains, e.g. .com. Consider
http://forums.bbc.co.uk: the naive splitting method
will give you "co" as the domain, instead of "bbc". Rather than juggle TLDs,
gTLDs, or ccTLDs  yourself, `tldextract` extracts the currently living public
suffixes according to the Public Suffix List.

> A "public suffix" is one under which Internet users can directly register
> names.

A public suffix is also sometimes called an effective TLD (eTLD).

## Usage

```python
>>> import tldextract

>>> tldextract.extract('http://forums.news.cnn.com/')
ExtractResult(subdomain='forums.news', domain='cnn', suffix='com', is_private=False)

>>> tldextract.extract('http://forums.bbc.co.uk/') # United Kingdom
ExtractResult(subdomain='forums', domain='bbc', suffix='co.uk', is_private=False)

>>> tldextract.extract('http://www.worldbank.org.kg/') # Kyrgyzstan
ExtractResult(subdomain='www', domain='worldbank', suffix='org.kg', is_private=False)
```

Note subdomain and suffix are _optional_. Not all URL-like inputs have a
subdomain or a valid suffix.

```python
>>> tldextract.extract('google.com')
ExtractResult(subdomain='', domain='google', suffix='com', is_private=False)

>>> tldextract.extract('google.notavalidsuffix')
ExtractResult(subdomain='google', domain='notavalidsuffix', suffix='', is_private=False)

>>> tldextract.extract('http://127.0.0.1:8080/deployed/')
ExtractResult(subdomain='', domain='127.0.0.1', suffix='', is_private=False)
```

To rejoin the original hostname, if it was indeed a valid, registered hostname:

```python
>>> ext = tldextract.extract('http://forums.bbc.co.uk')
>>> ext.registered_domain
'bbc.co.uk'
>>> ext.fqdn
'forums.bbc.co.uk'
```

By default, this package supports the public ICANN TLDs and their exceptions.
You can optionally support the Public Suffix List's private domains as well.

