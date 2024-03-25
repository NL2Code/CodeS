from grp import getgrgid
from pwd import getpwuid

from maybe import T, register_filter


def filter_change_owner(path, owner, group):
    if owner == -1:
        label = "change group"
        owner = getgrgid(group)[0]
    elif group == -1:
        label = "change owner"
        owner = getpwuid(owner)[0]
    else:
        label = "change owner"
        owner = getpwuid(owner)[0] + ":" + getgrgid(group)[0]
    return "%s of %s to %s" % (T.yellow(label), T.underline(path), T.bold(owner)), 0


register_filter(
    "chown",
    lambda process, args: filter_change_owner(
        process.full_path(args[0]), args[1], args[2]
    ),
)
register_filter(
    "fchown",
    lambda process, args: filter_change_owner(
        process.descriptor_path(args[0]), args[1], args[2]
    ),
)
register_filter(
    "lchown",
    lambda process, args: filter_change_owner(
        process.full_path(args[0]), args[1], args[2]
    ),
)
register_filter(
    "fchownat",
    lambda process, args: filter_change_owner(
        process.full_path(args[1], args[0]), args[2], args[3]
    ),
)
