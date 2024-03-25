import argparse
import os
import sys
from loguru import logger
import csv
import ast


parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str)
parser.add_argument("--output_path", type=str)

args = parser.parse_args()

input_dir = args.input_dir
output_path = args.output_path


def get_all_files(proj_path):
    files = []
    for dirpath, dirnames, filenames in os.walk(proj_path):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files


def extract_functions(source):
    lines = source.split("\n")
    start = 0
    function_sources = []
    while start < len(lines):
        line = lines[start]
        if line.startswith("def "):
            end = start + 1
            while True:
                if not lines[end].startswith(" ") and not lines[end].startswith("\t"):
                    function_sources.append("\n".join(lines[start:end]))
                    start = end
                    break
                end += 1
        start += 1
    return function_sources


def analyze_project(proj_path):
    file_cnt = 0
    code_line_cnt = 0
    function_cnt = 0
    proj_size = 0
    depth = 0
    for file in get_all_files(proj_path):
        if file.endswith(".py"):
            file_cnt += 1
            with open(file, "r") as f:
                code_line_cnt += len(f.readlines())
                proj_size += os.path.getsize(file)
                source = f.read()
                funcs = extract_functions(source)
                function_cnt += len(funcs)
            depth = max(depth, file[len(proj_path) :].count("/"))

    return file_cnt, code_line_cnt, function_cnt, proj_size, depth


proj_cnt = 0
results = []
for dirname in os.listdir(input_dir):
    if dirname == ".DS_Store":
        continue
    proj_cnt += 1
    proj_path = os.path.join(input_dir, dirname)
    file_cnt, code_line_cnt, function_cnt, proj_size, depth = analyze_project(proj_path)
    with open(output_path, "a") as f:
        results.append(
            {
                "project": dirname,
                "file_cnt": file_cnt,
                "code_line_cnt": code_line_cnt,
                "function_cnt": function_cnt,
                "proj_size": proj_size,
                "depth": depth,
            }
        )
    logger.info(f"Project {dirname} analyzed")

logger.info(f"Analyzed {proj_cnt} projects")
logger.info(f"Writing results to {output_path}")

results.sort(key=lambda x: x["code_line_cnt"], reverse=True)

with open(output_path, "w") as f:
    # write to csv
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)
