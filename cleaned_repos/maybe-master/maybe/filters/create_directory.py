from maybe import T, register_filter


def filter_create_directory(path):
    return "%s %s" % (T.cyan("create directory"), T.underline(path)), 0


register_filter(
    "mkdir", lambda process, args: filter_create_directory(process.full_path(args[0]))
)
register_filter(
    "mkdirat",
    lambda process, args: filter_create_directory(process.full_path(args[1], args[0])),
)
