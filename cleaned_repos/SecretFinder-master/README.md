# SecretFinder

SecretFinder is a python script based on LinkFinder, written to discover sensitive data like apikeys, accesstoken, authorizations, jwt,..etc in JavaScript files. It does so by using jsbeautifier for python in combination with a fairly large regular expression. The regular expressions consists of four small regular expressions. These are responsible for finding and search anything on js files.
The output is given in HTML or plaintext.

## Usage

- Most basic usage to find the sensitive data with default regex in an online JavaScript file and output the HTML results to results.html:

`python3 SecretFinder.py -i https://example.com/1.js -o results.html`

- CLI/STDOUT output (doesn't use jsbeautifier, which makes it very fast):

`python3 SecretFinder.py -i https://example.com/1.js -o cli`

- Analyzing an entire domain and its JS files:

`python3 SecretFinder.py -i https://example.com/ -e`

- Ignore certain js file (like external libs) provided by `-g --ignore`

`python3 SecretFinder.py -i https://example.com/ -e -g 'jquery;bootstrap;api.google.com'`

- Process only certain js file provided by `-n --only`:

`python3 SecretFinder.py -i https://example.com/ -e -n 'd3i4yxtzktqr9n.cloudfront.net;www.myexternaljs.com'`

- Use your regex:

`python3 SecretFinder.py -i https://example.com/1.js -o cli -r 'apikey=my.api.key[a-zA-Z]+'`

- Other options: add headers,proxy and cookies:

``python3 SecretFinder.py -i https://example.com/ -e -o cli -c 'mysessionid=111234' -H 'x-header:value1\nx-header2:value2' -p 127.0.0.1:8080 -r 'apikey=my.api.key[a-zA-Z]+'``

- Input accept all this entries:

 - Url: e.g. https://www.google.com/ [-e] is required
 - Js url: e.g. https://www.google.com/1.js
 - Folder: e.g. myjsfiles/*
 - Local file: e.g /js/myjs/file.js