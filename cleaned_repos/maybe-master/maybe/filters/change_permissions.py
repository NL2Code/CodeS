from maybe import T, register_filter


def format_permissions(permissions):
    result = ""
    for i in range(2, -1, -1):
        result += "r" if permissions & (4 * 8**i) else "-"
        result += "w" if permissions & (2 * 8**i) else "-"
        result += "x" if permissions & (1 * 8**i) else "-"
    return result


def filter_change_permissions(path, permissions):
    return (
        "%s of %s to %s"
        % (
            T.yellow("change permissions"),
            T.underline(path),
            T.bold(format_permissions(permissions)),
        ),
        0,
    )


register_filter(
    "chmod",
    lambda process, args: filter_change_permissions(
        process.full_path(args[0]), args[1]
    ),
)
register_filter(
    "fchmod",
    lambda process, args: filter_change_permissions(
        process.descriptor_path(args[0]), args[1]
    ),
)
register_filter(
    "fchmodat",
    lambda process, args: filter_change_permissions(
        process.full_path(args[1], args[0]), args[2]
    ),
)
