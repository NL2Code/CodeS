import logging
import sys

from .handout import Handout

logger = logging.getLogger("handout")
logger.setLevel(logging.INFO)
logger.propagate = False  # Global logger should not print messages again.
if not logger.handlers:  # Reloading the module should not add another handler.
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
