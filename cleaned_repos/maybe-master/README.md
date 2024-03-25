# `maybe`

It allows you to run a command and see what it does to your files *without actually doing it!* After reviewing the operations listed, you can then decide whether you really want these things to happen or not.

`maybe` runs processes under the control of ptrace (with the help of the excellent python-ptrace library). When it intercepts a system call that is about to make changes to the file system, it logs that call, and then modifies CPU registers to both redirect the call to an invalid syscall ID (effectively turning it into a no-op) and set the return value of that no-op call to one indicating success of the original call.

As a result, the process believes that everything it is trying to do is actually happening, when in reality nothing is.

That being said, `maybe` **should :warning: NEVER :warning: be used to run untrusted code** on a system you care about! A process running under `maybe` can still do serious damage to your system because only a handful of syscalls are blocked. It can also check whether an operation such as deleting a file succeeded using read-only syscalls, and *alter its behavior accordingly.* Therefore, a rerun without restrictions is not guaranteed to always produce the displayed operations.

Currently, `maybe` is best thought of as an (alpha-quality) "what exactly will this command I typed myself do?" tool.

### Example

Here, `maybe`'s plugin API is used to implement an exotic type of access control: Restricting read access based on the *content* of the file in question. If a file being opened for reading contains the word **SECRET**, the plugin blocks the `open`/`openat` syscall and returns an error.

#### `read_secret_file.py`

```python
from os import O_WRONLY
from os.path import isfile
from maybe import T, register_filter

def filter_open(path, flags):
    if path.startswith("/home/") and isfile(path) and not (flags & O_WRONLY):
        with open(path, "r") as f:
            if "SECRET" in f.read():
                return "%s %s" % (T.red("read secret file"), T.underline(path)), -1
            else:
                return None, None
    else:
        return None, None

register_filter("open", lambda process, args:
                filter_open(process.full_path(args[0]), args[1]))
register_filter("openat", lambda process, args:
                filter_open(process.full_path(args[1], args[0]), args[2]))
```

Indeed, the plugin works as expected:

```
[user@localhost]$ maybe --plugin read_secret_file.py --deny read_secret_file -- bash
$ echo "This is a normal file." > file_1
$ echo "This is a SECRET file." > file_2
$ cat file_1
This is a normal file.
$ cat file_2
cat: file_2: Operation not permitted
```