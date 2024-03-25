import utils
from transformers import AutoTokenizer
import transformers
import torch
import os
import sys
import json
from loguru import logger
import argparse
import pathlib
from tqdm import tqdm

sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.absolute()))
import prompt_construction_utils as prpt_utils

template = """[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n\n{} [/INST]"""

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=str, default=None)
parser.add_argument("--repo_dir", type=str, default="../cleaned_repos")
parser.add_argument(
    "--output_dir",
    type=str,
    default="../evaluation_results/from_scratch_inference_results",
)
parser.add_argument("--model", type=str, default=None)

args = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained(args.model)
pipeline = transformers.pipeline(
    "text-generation",
    model=args.model,
    torch_dtype=torch.float16,
    device_map="auto",
)

for repo in [args.project] if args.project else os.listdir(args.repo_dir):
    if not os.path.exists(os.path.join(args.repo_dir, repo, "README.md")):
        continue
    output_dir = os.path.join(args.output_dir, args.model.split("/")[-1], repo)
    if not os.path.exists(output_dir):
        os.system(f"mkdir -p {output_dir}")

    with open(os.path.join(output_dir, "repo_sketch.json"), "w") as f:
        with open(os.path.join(args.repo_dir, repo, "README.md"), "r") as f2:
            readme_content = f2.read().strip()
        json.dump(
            [
                {
                    "readme": readme_content,
                    "instruction": prpt_utils.get_repo_sketch_prompt(readme_content),
                }
            ],
            f,
        )

    for to_infer in ["repo_sketch.json", "file_sketch.json", "function_body.json"]:
        logger.info(f"Processing {repo} {to_infer}")
        input_file = os.path.join(output_dir, to_infer)
        with open(os.path.join(output_dir, to_infer), "r") as f:
            output_file = os.path.join(output_dir, to_infer + ".jsonl")
            with open(output_file, "w") as f1:
                pass

            with open(input_file, "r") as f1:
                data = json.load(f1)

            prepared_next_input = []
            insts = {}
            for each in tqdm(data):
                sequences = pipeline(
                    template.format(each["instruction"]),
                    do_sample=False,
                    num_return_sequences=1,
                    eos_token_id=tokenizer.eos_token_id,
                    pad_token_id=tokenizer.eos_token_id,
                    max_length=8192,
                    # max_new_tokens=2048,
                )

                for idx, seq in enumerate(sequences):
                    each["generated"] = (
                        seq["generated_text"].split("[/INST]")[-1].strip()
                    )
                    each["parsed"] = utils.parse_reponse(each["generated"])
                    with open(output_file, "a") as f1:
                        f1.write(json.dumps(each) + "\n")

                    if to_infer == "file_sketch.json":
                        insts[each["file_path"]] = each

                    if to_infer == "repo_sketch.json":
                        prepared_next_input.extend(
                            utils.generate_file_sketch_input(idx, each, readme_content)
                        )

            if to_infer == "file_sketch.json":
                for each in insts.values():
                    if each["file_path"].endswith(".py"):
                        prepared_next_input.extend(
                            utils.generate_function_body_input(
                                idx,
                                each,
                                readme_content,
                                insts,
                                "",
                            )
                        )

            next_input_file = None

            if to_infer == "repo_sketch.json":
                next_input_file = os.path.join(output_dir, "file_sketch.json")
            elif to_infer == "file_sketch.json":
                next_input_file = os.path.join(output_dir, "function_body.json")

            if next_input_file:
                with open(next_input_file, "w") as f1:
                    f1.write(json.dumps(prepared_next_input))
