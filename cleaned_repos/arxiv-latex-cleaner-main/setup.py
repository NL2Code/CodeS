from arxiv_latex_cleaner._version import __version__
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []
with open("requirements.txt") as f:
    for l in f.readlines():
        l_c = l.strip()
        if l_c and not l_c.startswith("#"):
            install_requires.append(l_c)

setup(
    name="arxiv_latex_cleaner",
    version=__version__,
    packages=find_packages(exclude=["*.tests"]),
    python_requires=">=3",
    url="https://github.com/google-research/arxiv-latex-cleaner",
    license="Apache License, Version 2.0",
    author="Google Research Authors",
    author_email="jponttuset@gmail.com",
    description="Cleans the LaTeX code of your paper to submit to arXiv.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": ["arxiv_latex_cleaner=arxiv_latex_cleaner.__main__:__main__"]
    },
    install_requires=install_requires,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Science/Research",
    ],
)
