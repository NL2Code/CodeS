# Firefox Decrypt

**Firefox Decrypt** is a tool to extract passwords from profiles of Mozilla (Fire/Water)fox™, Thunderbird®, SeaMonkey® and derivates.

It can be used to recover passwords from a profile protected by a Master Password as long as the latter is known.
If a profile is not protected by a Master Password, passwords are displayed without prompt.

This tool does not try to crack or brute-force the Master Password in any way.
If the Master Password is not known it will simply fail to recover any data.

It requires access to libnss3, included with most Mozilla products.
The script is usually able to find a compatible library but may in some cases
load an incorrect/incompatible version. If you encounter this situation please file a bug report.

If you need to decode passwords from Firefox 3 or older, although not officially supported,
there is a patch in this pull request.


## Usage

Run:

```
python firefox_decrypt.py
```

The tool will present a numbered list of profiles. Enter the relevant number. 

Then, a prompt to enter the *master password* for the profile: 

- if no password was set, no master password will be asked.
- if a password was set and is known, enter it and hit key <kbd>Return</kbd> or <kbd>Enter</kbd>
- if a password was set and is no longer known, you can not proceed