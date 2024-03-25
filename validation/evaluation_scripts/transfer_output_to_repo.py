import os
import sys
import json
import argparse
import ast
import astor
import black

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=str, default=None)
parser.add_argument("--input_dir", type=str, default="../outputs")
parser.add_argument(
    "--output_dir", type=str, default="../evaluation_results/transferred_repos"
)

args = parser.parse_args()

invalid_cases = []


class FillInFunction(ast.NodeTransformer):
    def __init__(self, function_map):
        super().__init__()
        self.function_map = function_map
        self.index = {}

    def visit_FunctionDef(self, node):
        if (
            node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, (ast.Str, ast.Constant))
        ):
            docstring = node.body[0]
        else:
            docstring = None

        if node.name in self.function_map.keys():
            if node.name not in self.index:
                self.index[node.name] = 0
            self.index[node.name] += 1
            function_source = self.function_map[node.name][self.index[node.name] - 1]
            while function_source.strip() != "":
                try:
                    node.body = ast.parse(function_source).body[0].body
                    break
                except:
                    function_source = "\n".join(function_source.split("\n")[:-1])

        return node


def fill_in_function(source_code, function_map):
    while source_code.strip() != "":
        try:
            parsed_code = ast.parse(source_code)
            break
        except:
            source_code = "\n".join(source_code.split("\n")[:-1])
    transformer = FillInFunction(function_map)
    new_code = transformer.visit(parsed_code)
    new_code = astor.to_source(new_code)

    new_code_beautified = black.format_str(new_code, mode=black.FileMode())

    return new_code_beautified.strip()


def get_functions(function_body_path):
    with open(function_body_path, "r") as f:
        lines = f.readlines()
        function_list = [json.loads(line) for line in lines]

    group_by_file = {}
    for function in function_list:
        if function["current_file_path"] not in group_by_file:
            group_by_file[function["current_file_path"]] = {}
        function_name = function["function_header"].split("(")[0].split("def ")[-1]
        if function_name not in group_by_file[function["current_file_path"]]:
            group_by_file[function["current_file_path"]][function_name] = []
        source = function["parsed"]
        if function["function_header"] in source:
            source = (
                function["function_header"]
                + source.split(function["function_header"])[-1]
            )
        group_by_file[function["current_file_path"]][function_name].append(source)

    return group_by_file


def get_files(file_sketch_path):
    with open(file_sketch_path, "r") as f:
        lines = f.readlines()
        file_list = [json.loads(line) for line in lines]

    file_sketch = {}
    for file in file_list:
        file_sketch[file["file_path"]] = file["parsed"]

    return file_sketch


if __name__ == "__main__":
    for repo in [args.project] if args.project else os.listdir(args.input_dir):
        input_dir = os.path.join(args.input_dir, repo)
        output_dir = os.path.join(args.output_dir, repo)
        file_sketch_path = os.path.join(input_dir, "file_sketch.json.jsonl")
        function_body_path = os.path.join(input_dir, "function_body.json.jsonl")
        if os.path.exists(output_dir):
            os.system(f"rm -rf {output_dir}")
        os.system(f"mkdir -p {output_dir}")

        function_group_by_file = get_functions(function_body_path)
        file_sketches = get_files(file_sketch_path)
        for relative_path in file_sketches.keys():
            file_sketch = file_sketches[relative_path]
            if relative_path not in function_group_by_file:
                new_file_sketch = file_sketch
            else:
                function_map = function_group_by_file[relative_path]
                invalid_cases = []
                new_file_sketch = fill_in_function(file_sketch, function_map)
                new_file_sketch = astor.to_source(ast.parse(new_file_sketch))
                for invalid_case in invalid_cases:
                    while invalid_case["source"].strip() != "":
                        try:
                            compile_success = ast.parse(invalid_case["source"])
                            break
                        except:
                            invalid_case["source"] = "\n".join(
                                invalid_case["source"].split("\n")[:-1]
                            )
                    new_file_sketch = new_file_sketch.replace(
                        invalid_case["old_source"].strip(),
                        invalid_case["source"].strip(),
                    )

            new_file_path = os.path.join(output_dir, relative_path)
            new_file_dir = os.path.dirname(new_file_path)
            if not os.path.exists(new_file_dir):
                os.system(f"mkdir -p {new_file_dir}")
            with open(new_file_path, "w") as f:
                f.write(new_file_sketch)
