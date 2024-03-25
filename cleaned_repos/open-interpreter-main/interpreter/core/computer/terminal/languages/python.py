import os

from .jupyter_language import JupyterLanguage

os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
# turn off colors in "terminal"
os.environ["ANSI_COLORS_DISABLED"] = "1"


class Python(JupyterLanguage):
    # Jupyter defaults to Python
    pass
