import json
import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))
import extract_sketch as sketch_utils
import prompt_construction_utils as prpt_utils


class RepoSketchNode:
    def __init__(self, name, annotation, indent):
        self.name = name
        self.annotation = annotation
        self.children = []
        self.indent = indent

    def add_child(self, child):
        self.children.append(child)

    def get_paths(self):
        if len(self.children) == 0:
            return [self.name]
        else:
            paths = []
            for child in self.children:
                paths += [
                    ((self.name + "/") if self.indent >= 0 else "") + path
                    for path in child.get_paths()
                ]
            return paths


def parse_repo_sketch(repo_sketch):
    lines = repo_sketch.split("\n")
    root_node = RepoSketchNode("root", "", -1)
    repo_sketch_nodes = [root_node]
    for line in lines:
        if line == "":
            continue
        line = (
            line.replace("\u251c", " ")
            .replace("\u2500", " ")
            .replace("\u2514", " ")
            .replace("\u2502", " ")
            .replace("|", " ")
        )
        i = 0
        while i < len(line) and line[i] == " ":
            i += 1
        indent_cnt = i
        if indent_cnt <= 0:
            continue
        name = line.strip()
        cur_node = RepoSketchNode(
            name.split("#")[0].strip(),
            name.split("#")[1].strip() if "#" in name else "",
            indent_cnt,
        )
        while (
            len(repo_sketch_nodes) != 0 and repo_sketch_nodes[-1].indent >= indent_cnt
        ):
            repo_sketch_nodes.pop()

        if len(repo_sketch_nodes) != 0:
            repo_sketch_nodes[-1].add_child(cur_node)

        repo_sketch_nodes.append(cur_node)

    return root_node


def parse_reponse(response):
    try:
        response = response.split("```")[1]
    except:
        pass
    response = "\n".join(response.split("\n")[1:])
    return response


def generate_file_sketch_input(idx, each, readme_content):
    repo_sketch_tree = parse_repo_sketch(each["parsed"])
    repo_sketch_paths = repo_sketch_tree.get_paths()
    file_sketch_insts = []
    for path in repo_sketch_paths:
        file_sketch_insts.append(
            {
                "idx": idx,
                "readme": readme_content,
                "repo_sketch": each["parsed"],
                "file_path": path,
                "instruction": prpt_utils.get_file_sketch_prompt(
                    readme_content, each["parsed"], path
                ),
            }
        )
    return file_sketch_insts


def generate_file_sketch_input_openai(each, readme_content, template):
    repo_sketch_tree = parse_repo_sketch(each["parsed"])
    repo_sketch_paths = repo_sketch_tree.get_paths()
    file_sketch_insts = []
    for path in repo_sketch_paths:
        if not path.endswith(".py"):
            continue
        file_sketch_insts.append(
            {
                "readme": readme_content,
                "repo_sketch": each["parsed"],
                "file_path": path,
                "instruction": template.format_map(
                    {
                        "readme": readme_content,
                        "repo_sketch": each["parsed"],
                        "file_path": path,
                    }
                ),
            }
        )
    return file_sketch_insts


def generate_function_body_input(idx, each, readme, insts, repo_path):
    python_content = each["parsed"]
    repo_sketch = each["repo_sketch"]
    repo_sketch_tree = parse_repo_sketch(repo_sketch)
    paths = repo_sketch_tree.get_paths()
    paths = [("", path) for path in paths]

    try:
        all_function_names = sketch_utils.get_all_function_names(python_content)
    except SyntaxError as e:
        print(e)
        while python_content != "":
            try:
                python_content = "\n".join(python_content.split("\n")[:-1])
                all_function_names = sketch_utils.get_all_function_names(python_content)
                break
            except:
                pass

    function_names_cnt = {}
    all_indexed_function_names = []
    for function_name in all_function_names:
        if function_name not in function_names_cnt:
            function_names_cnt[function_name] = 0
        function_names_cnt[function_name] += 1

        all_indexed_function_names.append(
            (function_names_cnt[function_name] - 1, function_name)
        )
    all_imports = sketch_utils.extract_imports(python_content)

    function_requets = []
    for idx, this_function_name in all_indexed_function_names:
        (
            relevant_file_list,
            relevant_file_sketch_content,
        ) = sketch_utils.get_relevant_file_meta(
            each["file_path"],
            all_imports,
            paths,
            this_function_name,
            repo_path,
            insts,
            idx,
        )

        readme_summary = sketch_utils.extract_summary_from_readme(readme)
        function_header_content = sketch_utils.extract_function_header(
            python_content, this_function_name, idx
        )
        prompt = prpt_utils.get_function_body_prompt(
            readme_summary,
            repo_sketch,
            relevant_file_sketch_content,
            function_header_content,
        )
        function_requets.append(
            {
                "idx": idx,
                "readme_summary": readme_summary,
                "repo_sketch": repo_sketch,
                "relevant_file_paths": relevant_file_list,
                "relevant_file_sketches": relevant_file_sketch_content,
                "current_file_path": each["file_path"],
                "function_header": function_header_content,
                "instruction": prompt,
            }
        )

    return function_requets


def generate_function_body_input_openai(each, readme, insts, repo_path, template):
    python_content = each["parsed"]
    repo_sketch = each["repo_sketch"]
    repo_sketch_tree = parse_repo_sketch(repo_sketch)
    paths = repo_sketch_tree.get_paths()
    paths = [("", path) for path in paths]

    try:
        all_function_names = sketch_utils.get_all_function_names(python_content)
    except SyntaxError as e:
        print(e)
        while python_content != "":
            try:
                python_content = "\n".join(python_content.split("\n")[:-1])
                all_function_names = sketch_utils.get_all_function_names(python_content)
                break
            except:
                pass

    # all_filted_function_names = sketch_utils.remove_duplicates(all_function_names)
    function_names_cnt = {}
    all_indexed_function_names = []
    for function_name in all_function_names:
        if function_name not in function_names_cnt:
            function_names_cnt[function_name] = 0
        function_names_cnt[function_name] += 1

        all_indexed_function_names.append(
            (function_names_cnt[function_name] - 1, function_name)
        )
    all_imports = sketch_utils.extract_imports(python_content)

    function_requets = []
    for idx, this_function_name in all_indexed_function_names:
        (
            relevant_file_list,
            relevant_file_sketch_content,
        ) = sketch_utils.get_relevant_file_meta(
            each["file_path"], all_imports, paths, this_function_name, repo_path, insts
        )

        readme_summary = sketch_utils.extract_summary_from_readme(readme)
        function_header_content = sketch_utils.extract_function_header(
            python_content, this_function_name
        )
        relevant_file_sketch_content = relevant_file_sketch_content.replace(
            "Relevant File Sketch", "## Relevant File Sketch"
        ).replace("Current File Sketch", "## Current File Sketch")
        relevant_file_sketch_content = (
            relevant_file_sketch_content.replace(
                "---\nHere is the file sketch of", "Here is the file sketch of"
            )
            .replace("---\n", "")
            .strip()
        )
        # splitted = relevant_file_sketch_content.split("\n")
        # splitted = [
        #     selected
        #     for selected in splitted
        #     if selected.strip() != "pass" and selected.strip() != '"""TODO"""'
        # ]
        # relevant_file_sketch_content = "\n".join(splitted)
        prompt = template.format_map(
            {
                "readme": readme_summary,
                "repo_sketch": repo_sketch,
                "file_sketches": relevant_file_sketch_content,
                "function_signature": function_header_content,
            }
        )
        function_requets.append(
            {
                "readme_summary": readme_summary,
                "repo_sketch": repo_sketch,
                "relevant_file_paths": relevant_file_list,
                "relevant_file_sketches": relevant_file_sketch_content,
                "current_file_path": each["file_path"],
                "function_header": function_header_content,
                "instruction": prompt,
            }
        )

    return function_requets


def parse_instruction(instruction):
    instruction = (
        instruction.replace("\n", " ")
        .replace("\t", " ")
        .replace("\r", " ")
        .replace("  ", " ")
        .strip()
    )
    return instruction
