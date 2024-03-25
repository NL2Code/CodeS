import json

from codebleu import calc_repobleu
from pathlib import Path
import argparse
from loguru import logger
from tokenize import tokenize, NUMBER, STRING, NAME, OP
from io import BytesIO
import csv

parser = argparse.ArgumentParser()
parser.add_argument(
    "--pred", type=str, required=True, help="Path to the predictions file."
)
parser.add_argument(
    "--ref", type=str, required=True, help="Path to the reference file."
)
parser.add_argument("--metric_file", type=str, required=False)
args = parser.parse_args()

repo_name = Path(args.ref).name


def tokenize_code(code):
    """Tokenize source code and return the list of tokens."""
    tokens = []
    try:
        for tok in tokenize(BytesIO(code.encode("utf-8")).readline):
            if tok.type == 57:  # TokenInfo.NEWLINE is 57 in Python 3.8
                tokens.append("\n")
            elif tok.type == 58:  # TokenInfo.INDENT is 58 in Python 3.8
                tokens.append("    ")
            elif tok.type == 59:  # TokenInfo.DEDENT is 59 in Python 3.8
                pass
            else:
                tokens.append(tok.string)
    except:
        pass
    return tokens


res = calc_repobleu(
    [Path(args.ref)], [Path(args.pred)], "python", tokenizer=tokenize_code
)

logger.info(res)

if args.metric_file and args.metric_file.endswith(".jsonl"):
    with open(args.metric_file, "a+") as f:
        res["repo"] = repo_name
        f.write(json.dumps(res) + "\n")
elif args.metric_file and args.metric_file.endswith(".csv"):
    res = {"repo": repo_name, **res}
    with open(args.metric_file, "a+") as f:
        writer = csv.DictWriter(f, fieldnames=res.keys())
        writer.writerow(res)
