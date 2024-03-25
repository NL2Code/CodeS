import sys
import os
import json
import csv

import argparse
from loguru import logger

parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", type=str)
parser.add_argument("--stats_path", type=str)

args = parser.parse_args()

output_dir = args.output_dir
stats_path = args.stats_path

for dirname in os.listdir(output_dir):
    if dirname == ".DS_Store":
        continue
    file_reqs = []
    func_reqs = []
    if os.path.isdir(os.path.join(output_dir, dirname)):
        logger.info(f"Processing {dirname}")
        with open(os.path.join(output_dir, dirname, "file_sketch.json"), "r") as f:
            file_reqs = json.loads(f.read())
        with open(os.path.join(output_dir, dirname, "function_body.json"), "r") as f:
            func_reqs = json.loads(f.read())
        with open(stats_path, "a+") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    dirname,
                    1,
                    len(file_reqs),
                    len(func_reqs),
                    1 + len(file_reqs) + len(func_reqs),
                ]
            )
    else:
        logger.info(f"Skipping {dirname}")
