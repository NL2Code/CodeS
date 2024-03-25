import re
import shlex
import subprocess


def query_xrandr():
    query = "xrandr --query"
    xrandr_output = subprocess.Popen(
        shlex.split(query), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, stderr = xrandr_output.communicate()
    return str(stdout, "utf-8")


def extract_displays(output):
    pattern = re.compile(r"\b({0})\b".format("connected"), flags=re.IGNORECASE)
    lines = output.splitlines()
    connected = [line for line in lines if pattern.search(line)]
    connected_displays = list(map(lambda display: display.split()[0], connected))
    return connected_displays


def detect_display_devices():
    """
    Detects available displays.
    returns connected_displays
    This contains the available device names compatible with xrandr
    """
    return extract_displays(query_xrandr())


if __name__ == "__main__":
    print(detect_display_devices())
