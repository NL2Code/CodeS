"""This module contains common utilities for the rest of the package.
"""
import random


LOREM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean sit amet nulla id mi imperdiet condimentum. \
           Vestibulum ac consequat lorem, eu tempus felis. Maecenas eget purus in nisi blandit volutpat. Aenean \
           bibendum eros sit amet ex rhoncus, eu porta magna sodales. Sed venenatis sapien sit amet tempor euismod. \
           Ut a neque purus. Vestibulum quis tortor non leo eleifend interdum."""


try:
    from loremipsum import get_sentence
except ImportError:
    def get_sentence():
        """This keeps the mess of dealing with the loremipsum library out of the shredding code. Until the maintainer of
        the loremipsum package uploads a version that works with Python 3 to pypi, it is necessary to provide a drop-in
        replacement. The current solution is to return a static text string unless the operating system has a word list.
        If that is the case, use it instead.
        """
        words = LOREM.split()
        random.shuffle(words)
        return " ".join(words)


class ShredditError(Exception):
    def __init__(self, value=None):
        self.value = value if value else "No information provided"

    def __str__(self):
        return repr(self.value)
