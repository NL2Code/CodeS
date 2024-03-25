# epubhv

epubhv is a tool to make your epub books vertical or horizontal or make them readable for language learners.

## Features

- Make your epub books vertical or horizontal
- Translate your epub books between `简体` and `繁体`
- Add `ruby` for Japanese(furigana) and Chinese(pinyin)
- Add `ruby` for `cantonese`

## Using pipx

If you are using [pipx](https://pypi.org/project/pipx/), you can directly run `epubhv` with:

```console
pipx run epubhv a.epub
```

## Use the web

```console
pip install epubhv[web]
streamlit run web.py
```

## Use CLI

```console
epubhv a.epub # will generate a file a-v.epub that is vertical
# or
epubhv b.epub --h # will generate a file b-h.epub that is horizontal

# if you also want to translate from `简体 -> 繁体`
epubhv c.epub --convert s2t

# if you also want to translate from `繁体 -> 简体`
epubhv d.epub --h --convert t2s

# or a folder contains butch of epubs
epubhv tests/test_epub # will generate all epub files to epub-v

# you can specify the punctuation style
epubhv e.epub --convert s2t --punctuation auto
# you can add `ruby` for Japanese(furigana) and Chinese(pinyin)
epubhv e.epub --h --ruby
# if you want to learn `cantonese` 粤语
epubhv f.epub --h --ruby --cantonese
```