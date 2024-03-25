import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent.absolute()))
import utils
import os
import json
from loguru import logger
import argparse
from tqdm import tqdm
from openai import OpenAI
import openai

TEMPLATE_DICT = {
    "repo_sketch.json": """You are a senior software engineer. You are asked to design a code repository sketch according to its README. This repository uses mainly the Python language.
Your response should be a repository tree formatting like the output of linux `tree` command. However, your response should also include the reference relationship between the code files. To address this goal, you can add the import statements behind each file represented in the repository tree to reflect the possible reference relationships. You can separate the file name and the import statements with a `#` mark. For example, if the file`a.py` import the file `b.py` and `c.py`, you should present `a.py` in the repository tree as `a.py # import b; import c`. So a simple example repository tree can be:
```
.
├── a.py # import dir1.b; import dir1.c
├── dir1
│   ├── b.py
│   └── c.py
└── README.md
```
You should design the repository sketch by observing the repository README, which will be give later.


## Repository README
```md
{readme}
```""",
    "file_sketch.json": """You are a senior software engineer. You are asked to design the sketch of a code file as a part of a code repository.
Your response should be a code snippet, which is the file sketch containing all the needed function signatures and other global statements (e.g. import statements, global variable declaration, and etc.). In a word, your response should be the content of a code file, but the functions are not necessarily implemented. You can replace the function body with jsut a `pass` statement.

You should design the file sketch according to the repository README and its structure. The path of the target file which you should implement is also given later.

## Repository README
```md
{readme}
```


## Repository Structure
```
{repo_sketch}
```


## Target File Path
{file_path}""",
    "function_body.json": """Please fill in the body of a Python function for a given code repository.
Your response should contain a ## Implemented Function. This part contains a code snippet, which is the implementation of the target function, including both the signature and the body.
For your reference, you will be given the ## Repository README, ## Repository Sketch, ## Relevant File Sketch and ## Current File Sketch. In the file sketches only the signature of all the functions are given. The target function is marked in the current file sketch with a \"""TODO\""" comment. You should understand what libraries or modules are used in the code file based on the provided sketches, and use them correctly in your response if needed. The target function to implement is also given later.


## Repository README
```md
{readme}
```


## Repository Structure
```
{repo_sketch}
```


{file_sketches}


## Target Function
{function_signature}""",
}

parser = argparse.ArgumentParser()
parser.add_argument("--project", type=str, default=None)
parser.add_argument("--repo_dir", type=str, default="../cleaned_repos")
parser.add_argument(
    "--output_dir",
    type=str,
    default="../evaluation_results/from_scratch_inference_results",
)
parser.add_argument("--model", type=str, default="gpt-3.5-turbo-1106")

args = parser.parse_args()

openai_api_base_url = os.environ.get("OPENAI_API_BASE_URL")
openai_api_key = os.environ.get("OPENAI_API_KEY")


def openai_request(instruction, temp=0.0):
    logger.info(f"temperature: {temp}")
    client = OpenAI(base_url=openai_api_base_url, api_key=openai_api_key)
    try:
        completion = client.chat.completions.create(
            model=args.model,
            temperature=temp,
            messages=[
                {"role": "user", "content": instruction},
            ],
        )
        logger.info(f"OpenAI API prompt: {instruction}")
        logger.info(f"OpenAI API response: {completion.choices[0].message}")
        return completion.choices[0].message.content
    except openai.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.OpenAIErrorAPIConnectionError as e:
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.OpenAIErrorRateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
    except openai.OpenAIErrorTimeout as e:
        print(f"OpenAI API request timed out: {e}")
        pass
    except openai.OpenAIErrorInvalidRequestError as e:
        print(f"Invalid request to OpenAI API: {e}")
        pass
    except openai.OpenAIErrorAuthenticationError as e:
        print(f"Authentication error with OpenAI API: {e}")
        pass
    except openai.OpenAIErrorServiceUnavailableError as e:
        print(f"OpenAI API service unavailable: {e}")
        pass

    return None


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
                    "instruction": TEMPLATE_DICT["repo_sketch.json"].format_map(
                        {"readme": readme_content}
                    ),
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
                sequence = None
                try_time = 5
                while sequence == None and try_time > 0:
                    try_time -= 1
                    sequence = openai_request(
                        each["instruction"], temp=0.0 if try_time == 4 else 0.1
                    )

                if sequence == None:
                    logger.error("can't connect to openai api")
                    exit(1)

                each["generated"] = sequence
                each["parsed"] = utils.parse_reponse(each["generated"])
                with open(output_file, "a") as f1:
                    f1.write(json.dumps(each) + "\n")

                if to_infer == "file_sketch.json":
                    insts[each["file_path"]] = each

                if to_infer == "repo_sketch.json":
                    prepared_next_input.extend(
                        utils.generate_file_sketch_input_openai(
                            each, readme_content, TEMPLATE_DICT["file_sketch.json"]
                        )
                    )

            if to_infer == "file_sketch.json":
                for each in insts.values():
                    if each["file_path"].endswith(".py"):
                        prepared_next_input.extend(
                            utils.generate_function_body_input_openai(
                                each,
                                readme_content,
                                insts,
                                "",
                                TEMPLATE_DICT["function_body.json"],
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
