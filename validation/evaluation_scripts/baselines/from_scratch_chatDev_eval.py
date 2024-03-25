import sys
import os
import argparse
from loguru import logger

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=str)
parser.add_argument("--input_dir", type=str)
parser.add_argument("--output_dir", type=str)

args = parser.parse_args()

project = args.project
input_dir = os.path.abspath(os.path.join(args.input_dir, project))
output_dir = os.path.abspath(os.path.join(args.output_dir, project))

if os.path.exists(output_dir):
    os.system(f"rm -r {output_dir}")

os.makedirs(output_dir)

readme_path = os.path.join(input_dir, "README.md")

os.system(
    f"cd ChatDev && python run.py --task {readme_path} --org codes --name {project}"
)

for dirname in os.listdir("ChatDev/WareHouse"):
    if dirname.startswith(project):
        project_dir = os.path.join("ChatDev/WareHouse", dirname)

for dirpath, dirnames, filenames in os.walk(project_dir):
    for filename in filenames:
        if filename.endswith(".py"):
            os.system(f"cp {os.path.join(dirpath, filename)} {output_dir}")

logger.info(f"Generated software for {project}")
