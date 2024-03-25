import subprocess

from trzsz.libs import utils


class ZenityProgressBar(utils.TrzszCallback):
    def __init__(self, action):
        self.num = 0
        self.idx = 0
        self.name = ""
        self.size = 0
        self.proc = None
        self.action = action
        self.progress = None

    def __del__(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None

    def on_num(self, num):
        self.num = num
        try:
            title = f"{self.action} file(s)"
            # pylint: disable-next=consider-using-with
            self.proc = subprocess.Popen(
                ["/usr/local/bin/zenity", "--progress", "--title", title, "--text", ""],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except EnvironmentError:
            pass

    def _update_progress(self, step):
        percentage = step * 100 // self.size if self.size else 0
        progress = f"{percentage}\n# {self.action} ( {self.idx} / {self.num} ) {percentage}% {self.name}\n"
        if progress == self.progress:
            return
        self.progress = progress
        self.proc.stdin.write(progress.encode("utf8"))
        self.proc.stdin.flush()

    def on_name(self, name):
        self.idx += 1
        self.size = 0
        self.name = name
        if not self.proc:
            return
        try:
            self._update_progress(0)
        except EnvironmentError:
            utils.stop_transferring()

    def on_size(self, size):
        self.size = size

    def on_step(self, step):
        if not self.proc:
            return
        try:
            self._update_progress(step)
        except EnvironmentError:
            if self.idx < self.num or step < self.size:
                utils.stop_transferring()

    def on_done(self):
        if not self.proc:
            return
        try:
            self._update_progress(self.size)
        except EnvironmentError:
            if self.idx < self.num:
                utils.stop_transferring()
        if self.idx == self.num:
            self.proc.terminate()
            self.proc = None
