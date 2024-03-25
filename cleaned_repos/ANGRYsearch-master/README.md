# ANGRYsearch
Linux file search, instant results as you type

Attempt at making Linux version of [Everything Search Engine](https://www.voidtools.com/) because no one else bothered.  
Everyone seems to be damn content with searches that are slow, populating results as they go; or are cli based, making it difficult to comfortably make use of the results; or are heavily integrated with a file manager, often limiting search to just home; or are trying to be everything with full-text file's content search.

### Lite mode vs Full mode

angrysearch can be set to two different modes in its config, default being `lite`
* **lite mode** shows only name and path
* **full mode** shows also size and date of the last modification, the drawback is that crawling through drives takes roughly twice as long since every file and directory gets additional stats calls

in `~/.config/angrysearch/angrysearch.conf` you control the mode with `angrysearch_lite` being set to true or false

### Search modes

there are 3 search modes, default being `fast`
* **fast mode** - enabled when the checkbox next to the input field is checked  
extremely fast, but no substrings, meaning it would not find "Pi<b>rate</b>s" or "Whip<b>lash</b>", but it would "<b>Pir</b>ates" or "The-<b>Fif</b>th"
* **slow mode** - enabled when the checkbox is unchecked, slightly slower but can find substrings, also very litteral with non typical characters
* **regex mode** - activated by the **F8** key, indicated by orange color background  
slowest search, used for very precise searches using [regular expressions](http://www.aivosto.com/vbtips/regex.html), set to case insensitive,  
unlike the previous search modes not entire path is searched, only the filenames/directory names