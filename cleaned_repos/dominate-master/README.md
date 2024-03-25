Dominate
========

`Dominate` is a Python library for creating and manipulating HTML documents using an elegant DOM API.
It allows you to write HTML pages in pure Python very concisely, which eliminates the need to learn another template language, and lets you take advantage of the more powerful features of Python.

Python:

```python
import dominate
from dominate.tags import *

doc = dominate.document(title='Dominate your HTML')

with doc.head:
    link(rel='stylesheet', href='style.css')
    script(type='text/javascript', src='script.js')

with doc:
    with div(id='header').add(ol()):
        for i in ['home', 'about', 'contact']:
            li(a(i.title(), href='/%s.html' % i))

    with div():
        attr(cls='body')
        p('Lorem ipsum..')

print(doc)
```

Output:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Dominate your HTML</title>
    <link href="style.css" rel="stylesheet">
    <script src="script.js" type="text/javascript"></script>
  </head>
  <body>
    <div id="header">
      <ol>
        <li>
          <a href="/home.html">Home</a>
        </li>
        <li>
          <a href="/about.html">About</a>
        </li>
        <li>
          <a href="/contact.html">Contact</a>
        </li>
      </ol>
    </div>
    <div class="body">
      <p>Lorem ipsum..</p>
    </div>
  </body>
</html>
```