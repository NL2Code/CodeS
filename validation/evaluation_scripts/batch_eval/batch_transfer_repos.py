import sys
import os

import argparse
from loguru import logger

parser = argparse.ArgumentParser()
parser.add_argument('--repo_dir', type=str)
parser.add_argument('--sketch_dir', type=str)
parser.add_argument('--output_dir', type=str)

args = parser.parse_args()

repo_dir = args.repo_dir
input_dir = args.sketch_dir
output_dir = args.output_dir

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for dirname  in os.listdir(repo_dir):
    cmd = f"python ../transfer_output_to_repo.py --project {dirname} --input_dir {input_dir} --output_dir {output_dir}"
    logger.info(cmd)
    os.system(cmd)
