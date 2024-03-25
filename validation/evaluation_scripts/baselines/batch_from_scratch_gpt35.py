import sys
import os

import argparse
from loguru import logger

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str)
parser.add_argument("--output_dir", type=str)

args = parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for dirname in os.listdir(input_dir):
    if dirname == ".DS_Store":
        continue
    cmd = f"python from_scratch_gpt35_eval.py --project {dirname} --repo_dir {input_dir} --output_dir {output_dir} --model gpt-3.5-turbo-0613"
    logger.info(cmd)
    os.system(cmd)
