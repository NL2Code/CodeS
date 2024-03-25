# Copyright (c) Huawei Cloud.
# Licensed under the MIT license.
import logging
import json
import sys
import os
import re
from tqdm import tqdm

import black
import ast
import astor
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.absolute()))
import prompt_construction_utils as prpt_util

repo_path = None

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def extract_imports(python_file_content):
    all_lines = python_file_content.split("\n")
    imports_list = []
    for line in all_lines:
        if line.startswith("import") or line.startswith("from"):
            imports_list.append(line)

    return imports_list


def load_imports(python_path):
    """
    Read a Python file and return a list of all imports.
    """
    with open(python_path, "r") as f:
        python_file_content = f.read()

    return extract_imports(python_file_content)


def zip_imports(imports_list):
    """
    Zip the imports list into a string prompt.
    """
    base_prompt = " # "
    for this_import in imports_list:
        base_prompt += this_import + "; "

    return base_prompt.strip()


def get_tree(directory, prefix="", tree_lists=[(".", "None")]):
    """
    Get the tree structure of the given directory.
    """
    files = []
    dirs = []
    items = os.listdir(directory)
    items.sort()  # Sort files and directories to maintain consistent order
    for item in items:
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            dirs.append(item)
        else:
            files.append(item)

    # Handle files in the current directory
    for index, item in enumerate(files):
        if item.endswith(".py") or item == "README.md" or item.endswith(".sh"):
            connector = "└── " if index == len(files) - 1 and not dirs else "├── "
            tree_lists.append(
                (prefix + connector + item, os.path.join(directory, item))
            )

    # Handle subdirectories in the current directory
    for index, item in enumerate(dirs):
        connector = "└── " if index == len(dirs) - 1 else "├── "
        tree_lists.append((prefix + connector + item, os.path.join(directory, item)))
        new_prefix = prefix + "    " if index == len(dirs) - 1 else prefix + "|   "
        get_tree(os.path.join(directory, item), new_prefix, tree_lists)

    return tree_lists


def get_tree_str(tree_lists):
    """
    Transform the tree lists into a string.
    """
    tree_str = ""
    for item, path in tree_lists:
        tree_str += item + "\n"
    return tree_str


def is_import_line_in_repo_sketch(import_line, tree_lists):
    """
    Judge whether the import line is in the repository sketch.
    """

    ignore_key_words = [
        "re",
        "json",
        "ast",
        "os",
        "socket",
        "typing",
        "dis",
        "io",
        "six",
        "config",
        "time",
        "logging",
        "unittest",
        "sys",
        "random",
        "pickle",
        "inspect",
        "subprocess",
        "multiprocessing",
        "threading",
        "collections",
        "functools",
        "math",
        "numpy",
        "pandas",
        "scipy",
        "sklearn",
        "torch",
        "tensorflow",
        "keras",
        "mxnet",
        "cntk",
        "jax",
        "chainer",
        "cupy",
        "paddle",
        "tvm",
        "onnx",
        "pytorch_lightning",
        "transformers",
        "nltk",
        "spacy",
        "gensim",
        "textblob",
        "jupyter",
        "matplotlib",
        "seaborn",
        "plotly",
        "bokeh",
        "dash",
        "streamlit",
        "pyecharts",
        "pydot",
        "graphviz",
        "pytorch_geometric",
        "dgl",
        "networkx",
        "scikit-image",
        "opencv-python",
        "pillow",
        "imageio",
        "scikit-learn",
        "string",
        "base64",
        "csv",
        "pygame",
    ]

    key_words = extract_key_names([import_line])

    # ipdb.set_trace()
    for key_word in key_words:
        if key_word in ignore_key_words:
            continue

        tree_str = get_tree_str(tree_lists)
        if key_word in tree_str:
            return True

    return False


def load_relevant_imports(python_path, tree_lists):
    """
    Get relevant imports from the given python file according to the repository sketch.
    """
    with open(python_path, "r") as f:
        python_file_content = f.read()

    all_lines = python_file_content.split("\n")
    imports_list = []  # all imports including public and repo-level ones
    for line in all_lines:
        if line.startswith("import") or line.startswith("from"):
            imports_list.append(line)

    # extract relevant imports
    relevant_imports = []
    for import_line in imports_list:
        if is_import_line_in_repo_sketch(import_line, tree_lists):
            if "version" not in import_line:
                relevant_imports.append(import_line)

    return relevant_imports


def add_imports_infos(tree_lists):
    new_tree_lists = []
    for name, path in tree_lists:
        if path.endswith(".py"):
            relevant_imports = load_relevant_imports(path, tree_lists)
            if len(relevant_imports) > 0:
                # print(relevant_imports)
                # ipdb.set_trace()
                name += " " + zip_imports(relevant_imports)

        new_tree_lists.append((name, path))

    return new_tree_lists


class FunctionNameCollector(ast.NodeVisitor):
    def __init__(self):
        self.function_names = []

    def visit_FunctionDef(self, node):
        self.function_names.append(node.name)
        self.generic_visit(node)


def get_all_function_names(source_code):
    """
    Get all function names from the given source code.
    """
    parsed_code = ast.parse(source_code)
    collector = FunctionNameCollector()
    collector.visit(parsed_code)

    return collector.function_names


class ReplaceFunctionBody(ast.NodeTransformer):
    def __init__(self, unimplemented_function_name="", index=0):
        super().__init__()
        self.unimplemented_function_name = unimplemented_function_name
        self.index = index

    def visit_FunctionDef(self, node):
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, (ast.Str, ast.Constant))
        ):
            docstring = node.body[0]
        else:
            docstring = None

        if node.name == self.unimplemented_function_name:
            if self.index > 0:
                self.index -= 1
            else:
                node.body = [ast.Expr(value=ast.Str(s="TODO"))]
        else:
            node.body = [ast.Pass()]

        if docstring:
            node.body.insert(0, docstring)

        return node


def replace_function_body(source_code, unimplemented_function_name="", index=0):
    """
    Get file sketch from the given source code by replacing the function body with "pass" or "TODO".
    """
    parsed_code = ast.parse(source_code)
    transformer = ReplaceFunctionBody(unimplemented_function_name, index)
    new_code = transformer.visit(parsed_code)
    new_code = astor.to_source(new_code)

    new_code_beautified = black.format_str(new_code, mode=black.FileMode())

    return new_code_beautified.strip()


def extract_key_names(all_imports):
    """
    Extract key names from all imports.
    """
    key_names = []
    for this_import in all_imports:
        for item in this_import.split(" "):
            if item == "import" or item == "from":
                continue
            elif item == "as":
                break
            else:
                if "." in item:
                    for this_item in item.split("."):
                        key_names.append(this_item)
                else:
                    key_names.append(item)
                break

    return key_names


def extract_relevant_file_paths(import_key_word_list, tree_lists):
    """
    Extract relevant file paths from the given path.
    """

    def parse_path_to_lists(path):
        kw_path_list = path.split("/")
        new_kw_path_list = []
        for index, item in enumerate(kw_path_list):
            if item == ".":
                continue
            if "." in item:
                new_kw_path_list.append(item.split(".")[0])
            else:
                new_kw_path_list.append(item)
        return new_kw_path_list

    relevant_file_paths = []
    for item, this_path in tree_lists:
        if not this_path.endswith(".py"):
            continue

        for key_word in import_key_word_list:
            if key_word in parse_path_to_lists(this_path):
                relevant_file_paths.append(this_path)
                break

    return relevant_file_paths


def get_relevant_final_prompt(
    path, relevant_file_paths, function_name, repo_path=repo_path, insts=None, index=0
):
    """
    Get the final prompt for relevant file sketch.
    """

    final_prompt = ""
    idx = 1

    for this_relevant_path in relevant_file_paths:
        if insts:
            this_python_content = insts[this_relevant_path]["parsed"]
        else:
            with open(this_relevant_path, "r") as f:
                this_python_content = f.read()

        this_python_file_sketch = ""
        while this_python_content.strip() != "":
            try:
                this_python_file_sketch = replace_function_body(this_python_content)
                break
            except:
                this_python_content = "\n".join(this_python_content.split("\n")[:-1])

        this_relevant_path = this_relevant_path[
            (len(repo_path) + 1) if len(repo_path) > 0 else 0 :
        ]
        final_prompt += prpt_util.get_relervant_file_sketch_content(
            idx, this_relevant_path, this_python_file_sketch
        )
        idx += 1

    if insts:
        python_content = insts[path]["parsed"]
    else:
        with open(path, "r") as f:
            python_content = f.read()
    while python_content.strip() != "":
        try:
            current_python_content = replace_function_body(
                python_content, function_name, index
            )
            break
        except:
            python_content = "\n".join(python_content.split("\n")[:-1])
    path = path[(len(repo_path) + 1) if len(repo_path) > 0 else 0 :]
    final_prompt += prpt_util.get_current_file_sketch_content(
        idx, path, current_python_content
    )

    return final_prompt


def get_relevant_file_sketch(path, all_imports, tree_lists, function_name, repo_path):
    import_key_word_list = extract_key_names(all_imports)
    relevant_file_paths = extract_relevant_file_paths(import_key_word_list, tree_lists)

    relevant_file_prompt = get_relevant_final_prompt(
        path, relevant_file_paths, function_name, repo_path
    )

    return relevant_file_prompt.strip()


def get_relevant_file_meta(
    path,
    all_imports,
    tree_lists,
    function_name,
    repo_path=repo_path,
    insts=None,
    index=0,
):
    import_key_word_list = extract_key_names(all_imports)
    relevant_file_paths = extract_relevant_file_paths(import_key_word_list, tree_lists)

    relevant_file_prompt = get_relevant_final_prompt(
        path, relevant_file_paths, function_name, repo_path, insts, index
    )

    return relevant_file_paths, relevant_file_prompt.strip()


def remove_duplicates(a):
    """
    Remove duplicates in a list.
    """
    duplicates = {x for x in a if a.count(x) > 1}
    unique_elements = [x for x in a if x not in duplicates]
    return unique_elements


def get_function_body(file_path, function_name):
    """
    Get function body from the given file path and function name.
    """
    with open(file_path, "r") as file:
        source_code = file.read()

    parsed_code = ast.parse(source_code)

    for node in ast.walk(parsed_code):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            try:
                source = astor.to_source(ast.Module(body=node.body)).strip()
            except Exception as e:
                print(f"cannot parse {file_path} {function_name}")
                print(ast.dump(node))
                print(e)
                return None

            return black.format_str(source, mode=black.FileMode())

    return None


def extract_function_header(python_content, this_function_name, index=0):
    all_lines = python_content.split("\n")
    header_lines = []
    flag = False
    for line in all_lines:
        if this_function_name in line and "def " in line:
            if index > 0:
                index -= 1
                continue
            header_lines.append(line)
            flag = True
        if flag == True and "def " not in line:
            header_lines.append(line)
        if flag == True and ":" in line:
            break

    assert (
        len(header_lines) > 0
    ), f"cannot find function header for {this_function_name}"
    function_header = "\n".join(header_lines)
    try:
        function_header_beatiful = (
            black.format_str(function_header.strip() + "pass", mode=black.FileMode())
            .replace("pass", "")
            .strip()
        )
        return function_header_beatiful
    except:
        return function_header.strip()


def get_function_header(path, this_function_name):
    """
    Get function header from the given file path and function name.
    """
    with open(path, "r") as f:
        python_content = f.read()

    return extract_function_header(python_content, this_function_name)


def add_four_spaces(a):
    """
    Add four spaces to each line in a string.
    """
    new_a = ""
    for line in a.split("\n"):
        new_a += "    " + line + "\n"
    return new_a


def extract_summary_from_readme(readme_content):
    """
    Extract the summary from a README file.
    """
    # with open(readme_file_path, 'r', encoding='utf-8') as file:
    #     readme_content = file.read()
    lines = readme_content.split("\n")

    summary = []
    header_count = 0

    for line in lines:
        if line.startswith("#"):
            header_count += 1
            if header_count > 1:
                break
        summary.append(line)

    return "\n".join(summary).strip()


def judge_a_content_empty(python_content):
    """
    Judge whether a Python file sketch is empty.
    """
    python_content = python_content.replace(
        "Here is a practicable file sketch.\n\n```python\n", ""
    ).replace("\n```", "")
    if python_content == "":
        return True

    lines = python_content.split("\n")
    for line in lines:
        if "import" in line or "from" in line or "as" in line:
            continue
        else:
            return False

    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Running extract sketch script for given repository."
    )
    parser.add_argument("--base_path", type=str, help="Path to repository.")
    parser.add_argument("--repo_names", type=str, help="Repository names.")
    parser.add_argument("--output_path", type=str, help="Path to save the sketch.")
    parser.add_argument(
        "--validation", action="store_true", help="Whether to generate validation data."
    )

    args = parser.parse_args()

    repo_names = args.repo_names.split(",")
    logging.info(f"processing {len(repo_names)} repositories")
    for repo_name in tqdm(repo_names, desc="repo_name"):
        repo_path = os.path.join(args.base_path, repo_name)
        logging.info(f"processing {repo_path}")

        # 1. getting readme content
        readme_content = ""
        readme_path = os.path.join(repo_path, "README.md")
        if os.path.exists(readme_path):
            with open(readme_path, "r") as f:
                readme_content = f.read()

        readme_content = readme_content.strip()

        tree_lists = [(".", "None")]
        tree_lists = get_tree(repo_path, "", tree_lists)

        tree_str = get_tree_str(tree_lists)
        # print(tree_str)
        # ipdb.set_trace()

        # logging.info(f"repo name: {repo_name}")
        # add repo-relevanted imports for each Python line
        tree_lists = add_imports_infos(tree_lists)

        # 2. getting repository sketch
        repo_sketch_content = ""
        for item, path in tree_lists:
            repo_sketch_content += item + "\n"

        repo_sketch_content = repo_sketch_content.strip()

        # ==============================
        # 1. repo sketch generation
        # ==============================
        json_path = os.path.join(args.output_path, repo_name, "repo_sketch.json")
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        repo_sketch_instruction = prpt_util.get_repo_sketch_prompt(readme_content)
        repo_sketch_output = f"""Here is a practicable repository sketch.

```
{repo_sketch_content}
```"""
        if args.validation:
            repo_sketch_list = [
                {
                    "readme": readme_content,
                    "instruction": repo_sketch_instruction,
                    "input": "",
                    "output": repo_sketch_output,
                }
            ]
        else:
            repo_sketch_list = [
                {
                    "instruction": repo_sketch_instruction,
                    "input": "",
                    "output": repo_sketch_output,
                }
            ]

        with open(json_path, "w+") as f:
            json.dump(repo_sketch_list, f, indent=4)

        logging.info(f"saved {len(repo_sketch_list)} repo sketch to {json_path}")

        # ==============================
        # 2. file sketch generation
        # ==============================
        file_sketch_path = os.path.join(args.output_path, repo_name, "file_sketch.json")
        file_sketch_list = []

        python_content = ""
        for item, path in tree_lists:
            if not path.endswith(".py") and not path.endswith(".sh"):
                continue

            with open(path, "r") as f:
                content = f.read()

            path = path.replace(repo_path, "")[1:]
            # get_all_function_names(python_content)
            file_sketch_instruction = prpt_util.get_file_sketch_prompt(
                readme_content, repo_sketch_content, path
            )
            if path.endswith(".py"):
                python_file_sketch = replace_function_body(content, "")
                if judge_a_content_empty(python_file_sketch):
                    continue
                # debugging
                # if "\n\n\n\n" in python_file_sketch:
                #     ipdb.set_trace()
                file_sketch_output = f"""Here is a practicable file sketch.

```python
{python_file_sketch}
```"""
            elif path.endswith(".sh"):
                file_content = content.strip()
                file_sketch_output = f"""Here is a practicable file content.

```bash
{file_content}
```"""

            if args.validation:
                file_sketch_list.append(
                    {
                        "readme": readme_content,
                        "repo_sketch": repo_sketch_content,
                        "file_path": path,
                        "instruction": file_sketch_instruction,
                        "input": "",
                        "output": file_sketch_output,
                    }
                )
            else:
                file_sketch_list.append(
                    {
                        "instruction": file_sketch_instruction,
                        "input": "",
                        "output": file_sketch_output,
                    }
                )

        with open(file_sketch_path, "w+") as f:
            json.dump(file_sketch_list, f, indent=4)

        logging.info(f"saved {len(file_sketch_list)} file sketch to {file_sketch_path}")

        # ==============================
        # 3. function body generation
        # ==============================
        function_body_path = os.path.join(
            args.output_path, repo_name, "function_body.json"
        )
        function_body_list = []

        for item, path in tree_lists:
            if not path.endswith(".py"):
                continue
            with open(path, "r") as f:
                python_content = f.read()

            all_function_names = get_all_function_names(python_content)
            all_filted_function_names = remove_duplicates(all_function_names)
            all_imports = load_imports(path)
            for this_function_name in all_filted_function_names:
                relevant_file_sketch_content = get_relevant_file_sketch(
                    path, all_imports, tree_lists, this_function_name, repo_path
                )

                # extract function header and function body
                # readme_content
                # repo_sketch_content
                # relevant_file_sketch_content
                function_body_content = get_function_body(path, this_function_name)
                if not function_body_content:
                    continue
                function_header_content = get_function_header(path, this_function_name)
                function_body_instruction = prpt_util.get_function_body_prompt(
                    extract_summary_from_readme(readme_content),
                    repo_sketch_content,
                    relevant_file_sketch_content,
                    function_header_content,
                )
                function_body_content_added_spaces = add_four_spaces(
                    function_body_content
                )
                function_header_body = (
                    function_header_content + "\n" + function_body_content_added_spaces
                )
                if (
                    function_header_body.strip() == ""
                    or function_body_content_added_spaces.strip() == ""
                    or function_body_content_added_spaces.strip() == "pass"
                ):
                    continue
                try:
                    function_header_body = black.format_str(
                        function_header_body, mode=black.FileMode()
                    ).strip()
                except:
                    pass

                function_body_output = f"""Here is a complete function body.

```python
{function_header_body}
```"""
                if args.validation:
                    relevant_file_meta = get_relevant_file_meta(
                        path, all_imports, tree_lists, this_function_name
                    )
                    function_body_list.append(
                        {
                            "readme": extract_summary_from_readme(readme_content),
                            "repo_sketch": repo_sketch_content,
                            "relevant_file_paths": [
                                x[(len(repo_path) + 1) if len(repo_path) > 0 else 0 :]
                                for x in relevant_file_meta[0]
                            ],
                            "relevant_file_sketches": relevant_file_meta[1],
                            "current_file_path": path[
                                (len(repo_path) + 1) if len(repo_path) > 0 else 0 :
                            ],
                            "instruction": function_body_instruction,
                            "input": "",
                            "output": function_body_output,
                        }
                    )
                else:
                    function_body_list.append(
                        {
                            "instruction": function_body_instruction,
                            "input": "",
                            "output": function_body_output,
                        }
                    )

        with open(function_body_path, "w+") as f:
            json.dump(function_body_list, f, indent=4)

        logging.info(
            f"saved {len(function_body_list)} function body to {function_body_path}"
        )

    logging.info(f"done!")