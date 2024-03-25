# trzsz

`trzsz` ( trz / tsz ) is a simple file transfer tools, similar to `lrzsz` ( rz / sz ), and compatible with `tmux`.

## Why?

Considering `laptop -> hostA -> hostB -> docker -> tmux`, using `scp` or `sftp` is inconvenience.

In this case, `lrzsz` ( rz / sz ) is convenient to use, but unfortunately it's not compatible with `tmux`.

`tmux` is not going to support rz / sz, and creating a new tools is much easier than patching `tmux`.

## Advantage

- Support **tmux**, including tmux normal mode, and tmux command mode integrated with iTerm2.
- Support **transfer directories**, `trz -d` to upload directories, `tsz -d xxx` to download xxx directories.
- Support **breakpoint resume**, `trz -y` or `tsz -y xxx` overwrite exiting files will auto resume from breakpoint.
- Support **Windows server**, not only can run on Windows client, but also can run on Windows ssh server.
- Support **native terminal**, does not require terminal to support, just use `trzsz ssh x.x.x.x` to login.
- Support **web terminal**, transfer files and directories between local and remote servers over the web.
- Support **drag to upload**, drag and drop files and directories to the terminal to upload to the remote server.
- Support **progress bar**, shows the current transferring file name, progress, size, speed, remaining time, etc.
- Better **interactive experience**, shows the transfer results or errors friendly, `ctrl + c` to stop gracefully.