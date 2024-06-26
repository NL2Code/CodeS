import json
import os
from argparse import ArgumentParser, FileType

from easierdocker.config import Config
from easierdocker.easier_docker import EasierDocker
from easierdocker.log_re import log


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        help="configuration file path: yaml, yml and json",
        required=True,
    )
    args = parser.parse_args()
    config_path = os.path.abspath(args.config) if args.config else None
    config = Config(config_path).load_file()
    log(
        f"config =\n {json.dumps(config, sort_keys=False, indent=4, separators=(',', ': '))}"
    )
    easier_docker = EasierDocker(config)
    easier_docker.start()


if __name__ == "__main__":
    main()
