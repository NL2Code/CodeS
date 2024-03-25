from setuptools import find_packages, setup

setup(
    name="gorilla-cli",
    version="0.0.11",
    url="https://github.com/gorilla-llm/gorilla-cli",
    author="Shishir Patil, Tianjun Zhang",
    author_email="sgp@berkeley.edu, tianjunz@berkeley.edu",
    description="LLMs for CLI",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    py_modules=["go_cli"],
    packages=find_packages(include=["*", "go_questionary.*"]),
    install_requires=[
        "requests",
        "halo",
        "prompt-toolkit",
    ],
    entry_points={
        "console_scripts": [
            "gorilla=go_cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache 2.0",
    python_requires=">=3.6",
)
