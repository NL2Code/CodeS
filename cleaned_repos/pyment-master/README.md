pyment
======

Create, update or convert docstrings in existing Python files, managing several styles.

Description
-----------

This Python3 program intends to help Python programmers to enhance inside code documentation using docstrings.
It is useful for code not well documented, or code without docstrings, or some not yet or partially documented code, or a mix of all of this :-)
It can be helpful also to harmonize or change a project docstring style format.

It will parse one or several python scripts and retrieve existing docstrings.
Then, for all found functions/methods/classes, it will generate formatted docstrings with parameters, default values,...

At the end, patches can be generated for each file. Then, man can apply the patches to the initial scripts.
It is also possible to update the files directly without generating patches, or to output on *stdout*. 
It is also possible to generate the python file with the new docstrings, or to retrieve only the docstrings...

Currently, the managed styles in input/output are javadoc, one variant of reST (re-Structured Text, used by Sphinx), numpydoc, google docstrings, groups (other grouped style).

You can also configure some settings via the command line or a configuration
file.

The tool, at the time, offer to generate patches or get a list of the new docstrings (created or converted).