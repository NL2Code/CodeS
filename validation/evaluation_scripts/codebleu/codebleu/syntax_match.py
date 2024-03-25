# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from typing import Union
from tree_sitter import Language, Parser, Node

from .parser import (
    DFG_csharp,
    DFG_go,
    DFG_java,
    DFG_javascript,
    DFG_php,
    DFG_python,
    DFG_ruby,
    remove_comments_and_docstrings,
)

dfg_function = {
    "python": DFG_python,
    "java": DFG_java,
    "ruby": DFG_ruby,
    "go": DFG_go,
    "php": DFG_php,
    "javascript": DFG_javascript,
    "c_sharp": DFG_csharp,
}


def calc_syntax_match(references, candidate, lang, lang_so_file):
    return corpus_syntax_match([references], [candidate], lang, lang_so_file)


def corpus_syntax_match(references, candidates, lang, lang_so_file):
    tree_sitter_language = Language(lang_so_file, lang)
    parser = Parser()
    parser.set_language(tree_sitter_language)
    match_count = 0
    match_count_candidate_to_reference = 0
    total_count = 0

    for i in range(len(candidates)):
        references_sample = references[i]
        candidate = candidates[i]
        for reference in references_sample:
            try:
                candidate = remove_comments_and_docstrings(candidate, lang)
            except Exception:
                pass
            try:
                reference = remove_comments_and_docstrings(reference, lang)
            except Exception:
                pass

            candidate_tree = parser.parse(bytes(candidate, "utf8")).root_node

            reference_tree = parser.parse(bytes(reference, "utf8")).root_node

            def get_all_sub_trees(root_node):
                node_stack = []
                sub_tree_sexp_list = []
                depth = 1
                node_stack.append([root_node, depth])
                while len(node_stack) != 0:
                    cur_node, cur_depth = node_stack.pop()
                    sub_tree_sexp_list.append([cur_node.sexp(), cur_depth])
                    for child_node in cur_node.children:
                        if len(child_node.children) != 0:
                            depth = cur_depth + 1
                            node_stack.append([child_node, depth])
                return sub_tree_sexp_list

            cand_sexps = [x[0] for x in get_all_sub_trees(candidate_tree)]
            ref_sexps = [x[0] for x in get_all_sub_trees(reference_tree)]
            print(type(cand_sexps[0]))
            print(ref_sexps)
            print("----------------")

            # TODO: fix, now we count number of reference subtrees matching candidate,
            #       but we should count number of candidate subtrees matching reference
            #       See (4) in "3.2 Syntactic AST Match" of https://arxiv.org/pdf/2009.10297.pdf
            for sub_tree in ref_sexps:
                if sub_tree in cand_sexps:
                    match_count += 1

            for sub_tree in cand_sexps:
                if sub_tree in ref_sexps:
                    match_count_candidate_to_reference += 1

            total_count += len(ref_sexps)
    # print(f'match_count       {match_count} / {total_count}')
    # print(f'match_count_fixed {match_count_candidate_to_reference} / {total_count}')
    score = match_count / total_count
    return score


import os
import re
from pathlib import Path


class RepoTree:
    def __init__(self, repo_dir: Path, parser):
        self.repo_dir = repo_dir
        self.parser = parser
        self.root = self.init_from_repo(repo_dir)

    def init_from_repo(self, repo_dir):
        self.root = FileOrNode("Root")
        for root, dirs, files in os.walk(repo_dir):
            for file in files:
                if file.endswith(".py"):
                    self.root.add_child(self.init_from_file(os.path.join(root, file)))
            for dir in dirs:
                self.root.add_child(self.init_from_dir(os.path.join(root, dir)))

        return self.root

    def init_from_dir(self, dir):
        ele = FileOrNode("Directory")
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".py"):
                    self.root.add_child(self.init_from_file(os.path.join(root, file)))
            for dir in dirs:
                self.root.add_child(self.init_from_dir(os.path.join(root, dir)))

        return ele

    def init_from_file(self, file):
        ele = FileOrNode("File")
        with open(file, "r", encoding="utf8", errors="ignore") as f:
            code = f.read()
        code = remove_comments_and_docstrings(code, "utf8")
        tree = self.parser.parse(bytes(code, "utf8")).root_node
        cursor = tree.walk()
        if cursor.goto_first_child():
            child_nodes = []
            while cursor.goto_next_sibling():
                child_nodes.append(FileOrNode(cursor.node))
            for idx in range(len(child_nodes)):
                ele.add_child(child_nodes[idx])

        return ele

    def get_all_sub_tree_nodes(self):
        node_stack = [self.root]
        all_nodes = []
        while len(node_stack) != 0:
            cur_node = node_stack.pop()
            all_nodes.append(cur_node)
            if cur_node.children is not None:
                for child_node in cur_node.children:
                    node_stack.append(child_node)
            elif isinstance(cur_node.labelOrNode, Node):
                for child_node in cur_node.labelOrNode.children:
                    node_stack.append(FileOrNode(child_node))

        return all_nodes


class FileOrNode:
    def __init__(self, labelOrNode: Union[str, Node]):
        self.labelOrNode = labelOrNode
        self.children = None
        if isinstance(self.labelOrNode, str):
            self.children = []

    def __eq__(self, other):
        if isinstance(other, FileOrNode):
            return self.to_str == other.to_str
        else:
            return False

    def __hash__(self):
        return hash(self.labelOrNode)

    def add_child(self, Node):
        assert self.children is not None
        self.children.append(Node)

    def to_str(self, depth=3):
        escaped = ["identifier", "string_content", "string_end", "string_start", "block"]
        if (
            isinstance(self.labelOrNode, Node)
            and self.labelOrNode.child_count + self.labelOrNode.named_child_count == 0
            and self.labelOrNode.type not in escaped
        ):
            return ""
        if depth == 1:
            if isinstance(self.labelOrNode, str):
                return f"({self.labelOrNode})"
            else:
                return f"({self.labelOrNode.type})"

        if isinstance(self.labelOrNode, str):
            assert self.children is not None
            if len(self.children) == 0:
                return f"({self.labelOrNode})"
            else:
                segs = [x.to_str(depth - 1) for x in self.children]
                segs = [x for x in segs if x != ""]
                return f"({self.labelOrNode} {' '.join(segs)})"
        else:
            cursor = self.labelOrNode.walk()
            if cursor.goto_first_child():
                field_names = []
                child_nodes = []
                if cursor.node.child_count + cursor.node.named_child_count != 0 or cursor.node.type in escaped:
                    field_names.append(cursor.field_name)
                    child_nodes.append(FileOrNode(cursor.node))
                while cursor.goto_next_sibling():
                    if cursor.node.child_count + cursor.node.named_child_count != 0 or cursor.node.type in escaped:
                        field_names.append(cursor.field_name)
                        child_nodes.append(FileOrNode(cursor.node))
                segs = []
                for idx in range(len(field_names)):
                    if field_names[idx] is not None:
                        segs.append(f"{field_names[idx]}: {child_nodes[idx].to_str(depth-1)}")
                    else:
                        segs.append(child_nodes[idx].to_str(depth - 1))
                segs = [x for x in segs if x != ""]
                if len(segs) == 0:
                    return f"({self.labelOrNode.type})"
                return f"({self.labelOrNode.type} {' '.join(segs)})"
            else:
                return f"({self.labelOrNode.type})"


def repo_syntax_match(references, candidates, lang, lang_so_file):
    tree_sitter_language = Language(lang_so_file, lang)
    parser = Parser()
    parser.set_language(tree_sitter_language)
    match_count = 0
    match_count_candidate_to_reference = 0
    total_count = 0

    for i in range(len(candidates)):
        references_sample = references[i]
        candidate = candidates[i]
        candidate_tree = RepoTree(candidate, parser)
        for reference in references_sample:
            reference_tree = RepoTree(reference, parser)

            def get_all_sub_trees(repo_tree):
                all_nodes = repo_tree.get_all_sub_tree_nodes()
                sub_tree_sexp_list = [x.to_str() for x in all_nodes]
                sub_tree_sexp_list = [x for x in sub_tree_sexp_list if x != ""]
                sub_tree_sexp_list = [x for x in sub_tree_sexp_list if re.search(r"\(.*\(.*\).*\)", x) is not None]
                return sub_tree_sexp_list

            cand_sexps = get_all_sub_trees(candidate_tree)
            ref_sexps = get_all_sub_trees(reference_tree)

            # TODO: fix, now we count number of reference subtrees matching candidate,
            #       but we should count number of candidate subtrees matching reference
            #       See (4) in "3.2 Syntactic AST Match" of https://arxiv.org/pdf/2009.10297.pdf
            for sub_tree in ref_sexps:
                if sub_tree in cand_sexps:
                    match_count += 1

            for sub_tree in cand_sexps:
                if sub_tree in ref_sexps:
                    match_count_candidate_to_reference += 1

            total_count += len(ref_sexps)
    # print(f'match_count       {match_count} / {total_count}')
    # print(f'match_count_fixed {match_count_candidate_to_reference} / {total_count}')
    score = match_count / total_count
    return score
