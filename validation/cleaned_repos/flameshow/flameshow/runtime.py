"""
Holds the run time configs.
Can be changed dynamically.
"""

import logging
from dataclasses import dataclass

from .colors import flamegraph_random_color_platte

logger = logging.getLogger(__name__)


@dataclass
class Runtime:
    color_platte = flamegraph_random_color_platte

    def get_color(self, key):
        return self.color_platte.get_color(key)


r = Runtime()
