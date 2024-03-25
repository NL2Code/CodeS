# =============非常慢的方式=============
from transformers import AutoTokenizer
import transformers
import torch
import os
import sys
import json
from loguru import logger
import argparse
from tqdm import tqdm

template = """[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. 

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n\n{} [/INST]"""

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=str, default=None)
parser.add_argument("--input_dir", type=str, default="../outputs")
parser.add_argument(
    "--output_dir", type=str, default="../evaluation_results/inference_results"
)
parser.add_argument("--phase", type=str, default=None)
parser.add_argument("--model", type=str, default=None)

args = parser.parse_args()

tokenizer = AutoTokenizer.from_pretrained(args.model)
pipeline = transformers.pipeline(
    "text-generation",
    model=args.model,
    torch_dtype=torch.float16,
    device_map="auto",
)

for repo in [args.project] if args.project else os.listdir(args.input_dir):
    output_dir = os.path.join(args.output_dir, args.model.split("/")[-1], repo)
    if not os.path.exists(output_dir):
        os.system(f"mkdir -p {output_dir}")
    for to_infer in (
        ["repo_sketch.json", "file_sketch.json", "function_body.json"]
        if not args.phase
        else f"{args.phase}.json"
    ):
        logger.info(f"Processing {repo} {to_infer}")
        input_file = os.path.join(args.input_dir, repo, to_infer)
        with open(os.path.join(args.input_dir, repo, to_infer), "r") as f:
            output_file = os.path.join(output_dir, to_infer + ".jsonl")
            with open(output_file, "w") as f:
                pass

            with open(input_file, "r") as f:
                data = json.load(f)

            for each in tqdm(data):
                sequences = pipeline(
                    template.format(each["instruction"]),
                    do_sample=False,
                    num_return_sequences=1,
                    eos_token_id=tokenizer.eos_token_id,
                    max_length=8192,
                    # max_new_tokens=2048,
                )
                each["generated"] = (
                    sequences[0]["generated_text"].split("[/INST]")[-1].strip()
                )
                for seq in sequences:
                    with open(output_file, "a") as f:
                        f.write(json.dumps(each) + "\n")

# =============使用VLLM加速之后的推理方式，快很多=============
# from vllm import LLM, SamplingParams

# # Sample prompts.
# prompts = [
#     raw_input
# ]
# # Create a sampling params object.
# sampling_params = SamplingParams(
#   temperature=0.8,
#   top_p=0.95,
#   max_tokens=1024
# )

# # Create an LLM.
# llm = LLM(model="/dev/shm/codes7b/full/2024-01-01-00-00-01/checkpoint-5")
# # Generate texts from the prompts. The output is a list of RequestOutput objects
# # that contain the prompt, generated text, and other information.
# outputs = llm.generate(prompts, sampling_params)
# # Print the outputs.
# for output in outputs:
#     prompt = output.prompt
#     generated_text = output.outputs[0].text
#     print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
