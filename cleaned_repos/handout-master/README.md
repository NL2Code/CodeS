# Python Handout

Turn Python scripts into handouts with Markdown comments and inline figures. An
alternative to Jupyter notebooks without hidden state that supports any text
editor.

## Features

Create the handout via `doc = handout.Handout(outdir)` to access these features:

| Feature | Example |
| ------- | ------- |
| Add Markdown text as triple-quote comments. | `"""Markdown text"""` |
| Add text via `print()` syntax. | `doc.add_text('text:', variable)` |
| Add image from array or url. | `doc.add_image(image, 'png', width=1)` |
| Add video from array or url. | `doc.add_video(video, 'gif', fps=30, width=1)` |
| Add matplotlib figure. | `doc.add_figure(fig, width=1)` |
| Add custom HTML. | `doc.add_html(string)` |
| Insert added items and save to `<outdir>/index.html`. | `doc.show()` |