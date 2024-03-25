# PySnooper - Never use print for debugging again

**PySnooper** is a poor man's debugger. If you've used Bash, it's like `set -x` for Python, except it's fancier.

Your story: You're trying to figure out why your Python code isn't doing what you think it should be doing. You'd love to use a full-fledged debugger with breakpoints and watches, but you can't be bothered to set one up right now.

You want to know which lines are running and which aren't, and what the values of the local variables are.

Most people would use `print` lines, in strategic locations, some of them showing the values of variables.

**PySnooper** lets you do the same, except instead of carefully crafting the right `print` lines, you just add one decorator line to the function you're interested in. You'll get a play-by-play log of your function, including which lines ran and   when, and exactly when local variables were changed.

What makes **PySnooper** stand out from all other code intelligence tools? You can use it in your shitty, sprawling enterprise codebase without having to do any setup. Just slap the decorator on, as shown below, and redirect the output to a dedicated log file by specifying its path as the first argument.

## Features

If stderr is not easily accessible for you, you can redirect the output to a file:

```python
@pysnooper.snoop('/my/log/file.log')
```

You can also pass a stream or a callable instead, and they'll be used.

See values of some expressions that aren't local variables:

```python
@pysnooper.snoop(watch=('foo.bar', 'self.x["whatever"]'))
```

Show snoop lines for functions that your function calls:

```python
@pysnooper.snoop(depth=2)
```