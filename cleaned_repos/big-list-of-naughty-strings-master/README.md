# Big List of Naughty Strings
The Big List of Naughty Strings is an evolving list of strings which have a high probability of causing issues when used as user-input data. This is intended for use in helping both automated and manual QA testing; useful for whenever your QA engineer walks into a bar.

## Why Test Naughty Strings?

Even multi-billion dollar companies with huge amounts of automated testing can't find every bad input. 

Although this is not a malicious error, and typical users aren't Tweeting weird unicode, an "internal server error" for unexpected input is never a positive experience for the user, and may in fact be a symptom of deeper string-validation issues. The Big List of Naughty Strings is intended to help reveal such issues.

## Usage

`blns.txt` consists of newline-delimited strings and comments which are preceded with `#`. The comments divide the strings into sections for easy manual reading and copy/pasting into input forms. For those who want to access the strings programmatically, a `blns.json` file is provided containing an array with all the comments stripped out (the `scripts` folder contains a Python script used to generate the `blns.json`).