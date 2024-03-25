# better-exceptions

Pretty and more helpful exceptions in Python, automatically.

## Usage

Install `better_exceptions` via pip:

```console
pip install better_exceptions
```

And set the `BETTER_EXCEPTIONS` environment variable to any value:

```bash
export BETTER_EXCEPTIONS=1  # Linux / OSX
setx BETTER_EXCEPTIONS 1    # Windows
```

That's it!

### Python REPL (Interactive Shell)

In order to use `better_exceptions` in the Python REPL, first install the package (as instructed above) and run:

```console
$ python -m better_exceptions
Type "help", "copyright", "credits" or "license" for more information.
(BetterExceptionsConsole)
>>>
```

in order to drop into a `better_exceptions`-enabled Python interactive shell.