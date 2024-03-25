# AWS CloudFormation Template Flip

## About

AWS CloudFormation Template Flip is a tool that converts AWS CloudFormation templates between JSON and YAML formats, making use of the YAML format's short function syntax where possible.

The term "Flip" is inspired by the well-known Unix command-line tool flip which converts text files between Unix, Mac, and MS-DOS formats.

## Usage

AWS CloudFormation Template Flip is both a command line tool and a python library.

Note that the command line tool is spelled `cfn-flip` with a hyphen, while the python package is `cfn_flip` with an underscore.

### Python package

To use AWS CloudFormation Template Flip from your own python projects, import one of the functions `flip`, `to_yaml`, or `to_json` as needed.

```python
from cfn_flip import flip, to_yaml, to_json

"""
All functions expect a string containing serialised data
and return a string containing serialised data
or raise an exception if there is a problem parsing the input
"""

# flip takes a best guess at the serialisation format
# and returns the opposite, converting json into yaml and vice versa
some_yaml_or_json = flip(some_json_or_yaml)

# to_json expects serialised yaml as input, and returns serialised json
some_json = to_json(some_yaml)

# to_yaml expects serialised json as input, and returns serialised yaml
some_yaml = to_yaml(some_json)

# The clean_up flag performs some opinionated, CloudFormation-specific sanitation of the input
# For example, converting uses of Fn::Join to Fn::Sub
# flip, to_yaml, and to_json all support the clean_up flag
clean_yaml = to_yaml(some_json, clean_up=True)
```