import sys
import os

import argparse
from loguru import logger

parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", type=str)
parser.add_argument("--valid_dir", type=str)

args = parser.parse_args()

valid_dir = args.valid_dir
output_dir = args.output_dir

for dirname in os.listdir(valid_dir):
    if dirname == ".DS_Store":
        continue
    cmd = f"python get_metric.py --pred {output_dir}/{dirname} --ref {valid_dir}/{dirname} --metric_file {output_dir}/metrics.csv"
    logger.info(cmd)
    os.system(cmd)
