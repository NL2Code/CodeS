# `arxiv_latex_cleaner`

This tool allows you to easily clean the LaTeX code of your paper to submit to
arXiv. From a folder containing all your code, e.g. `/path/to/latex/`, it
creates a new folder `/path/to/latex_arXiv/`, that is ready to ZIP and upload to
arXiv.

## Example call:

```bash
arxiv_latex_cleaner /path/to/latex --resize_images --im_size 500 --images_allowlist='{"images/im.png":2000}'
```

Or simply from a config file

```bash
arxiv_latex_cleaner /path/to/latex --config cleaner_config.yaml
```