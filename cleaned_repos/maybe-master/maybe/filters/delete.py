from maybe import T, register_filter


def filter_delete(path):
    return "%s %s" % (T.red("delete"), T.underline(path)), 0


register_filter(
    "unlink", lambda process, args: filter_delete(process.full_path(args[0]))
)
register_filter(
    "unlinkat", lambda process, args: filter_delete(process.full_path(args[1], args[0]))
)
register_filter(
    "rmdir", lambda process, args: filter_delete(process.full_path(args[0]))
)
