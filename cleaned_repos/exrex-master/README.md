EXREX
=====

Irregular methods for regular expressions.

Exrex is a command line tool and python module that generates all - or random - matching strings to a given regular expression and more.
It's pure python, without external dependencies.

There are regular expressions with infinite matching strings (eg.: `[a-z]+`), in these cases exrex limits the maximum length of the infinite parts.

Exrex uses generators, so the memory usage does not depend on the number of matching strings.

*Features*

 * Generating all matching strings
 * Generating a random matching string
 * Counting the number of matching strings
 * Simplification of regular expressions