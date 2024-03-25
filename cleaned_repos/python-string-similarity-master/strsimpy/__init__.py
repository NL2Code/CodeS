from .cosine import Cosine
from .damerau import Damerau
from .jaccard import Jaccard
from .levenshtein import Levenshtein
from .longest_common_subsequence import LongestCommonSubsequence
from .metric_lcs import MetricLCS
from .ngram import NGram
from .normalized_levenshtein import NormalizedLevenshtein
from .optimal_string_alignment import OptimalStringAlignment
from .qgram import QGram
from .shingle_based import ShingleBased
from .sift4 import SIFT4, SIFT4Options
from .sorensen_dice import SorensenDice
from .string_distance import StringDistance
from .string_similarity import StringSimilarity
from .weighted_levenshtein import WeightedLevenshtein

__name__ = "strsimpy"
__version__ = "0.2.1"
