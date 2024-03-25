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
    cmd = f"python from_scratch_chatDev_eval.py --project {dirname} --input_dir {input_dir} --output_dir {output_dir}"
    logger.info(cmd)
    os.system(cmd)
