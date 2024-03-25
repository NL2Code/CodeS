import re

from setuptools import find_packages, setup

VERSION_REGEX = r'[ \t]*__version__[ \t]*=[ \t]*[\'"](\d+\.\d+\.\d+)[\'"]'
with open("trzsz/svr/__version__.py", "r") as file:
    version = re.search(VERSION_REGEX, file.read()).group(1)

with open("README.md", "rb") as file:
    long_description = file.read().decode("utf8")

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: MacOS",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Topic :: Utilities",
]

entry_points = {
    "console_scripts": [
        "trz = trzsz.svr.recv:main",
        "tsz = trzsz.svr.send:main",
    ],
}

setup(
    name="trzsz-svr",
    version=version,
    author="Lonny Wong",
    author_email="lonnywong@qq.com",
    packages=find_packages(),
    namespace_packages=["trzsz"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://trzsz.github.io",
    install_requires=["trzsz-libs == " + version],
    license="MIT License",
    classifiers=classifiers,
    entry_points=entry_points,
    keywords="trzsz trz tsz lrzsz rz sz tmux iTerm2 progressbar",
    zip_safe=False,
    description="trzsz is a simple file transfer tools, "
    "similar to lrzsz ( rz / sz ) and compatible with tmux, "
    "which works with iTerm2 and has a nice progress bar.",
)
