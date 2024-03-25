import icecream

try:
    builtins = __import__("__builtin__")
except ImportError:
    builtins = __import__("builtins")


def install(ic="ic"):
    setattr(builtins, ic, icecream.ic)


def uninstall(ic="ic"):
    delattr(builtins, ic)
