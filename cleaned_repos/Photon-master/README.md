# Photon

<h4 align="center">Incredibly fast crawler designed for OSINT.</h4>

### Key Features

#### Data Extraction
Photon can extract the following data while crawling:

- URLs (in-scope & out-of-scope)
- URLs with parameters (`example.com/gallery.php?id=2`)
- Intel (emails, social media accounts, amazon buckets etc.)
- Files (pdf, png, xml etc.)
- Secret keys (auth/API keys & hashes)
- JavaScript files & Endpoints present in them
- Strings matching custom regex pattern
- Subdomains & DNS related data

#### Flexible
Control timeout, delay, add seeds, exclude URLs matching a regex pattern and other cool stuff.
The extensive range of options provided by Photon lets you crawl the web exactly the way you want.

#### Genius
Photon's smart thread management & refined logic gives you top notch performance.

Still, crawling can be resource intensive but Photon has some tricks up it's sleeves. You can fetch URLs archived by archive.org to be used as seeds by using `--wayback` option.