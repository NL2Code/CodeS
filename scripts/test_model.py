instruction = """[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature. 

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n\n{} [/INST]"""
print(instruction)

raw_input = """Below is a detailed README.md of repository. Please write a repository sketch in the form of a tree, including all folders, files, as well as imports information if necessary.

---
README.md
---
# epubhv

epubhv is a tool to make your epub books vertical or horizontal or make them readable for language learners.

## Features

- Make your epub books vertical or horizontal
- Translate your epub books between `简体` and `繁体`
- Add `ruby` for Japanese(furigana) and Chinese(pinyin)
- Add `ruby` for `cantonese`

## Using pipx

If you are using [pipx](https://pypi.org/project/pipx/), you can directly run `epubhv` with:

```console
pipx run epubhv a.epub
```

## Use the web

```console
pip install epubhv[web]
streamlit run web.py
```

## Use CLI

```console
epubhv a.epub # will generate a file a-v.epub that is vertical
# or
epubhv b.epub --h # will generate a file b-h.epub that is horizontal

# if you also want to translate from `简体 -> 繁体`
epubhv c.epub --convert s2t

# if you also want to translate from `繁体 -> 简体`
epubhv d.epub --h --convert t2s

# or a folder contains butch of epubs
epubhv tests/test_epub # will generate all epub files to epub-v

# you can specify the punctuation style
epubhv e.epub --convert s2t --punctuation auto
# you can add `ruby` for Japanese(furigana) and Chinese(pinyin)
epubhv e.epub --h --ruby
# if you want to learn `cantonese` 粤语
epubhv f.epub --h --ruby --cantonese
```

---
Repository Sketch
---
"""

prompt = instruction.format(raw_input)

from transformers import AutoTokenizer
import transformers
import torch

model = "/dev/shm/codes7b/full/2024-01-19-00-00-02/checkpoint-150"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto"
)

sequences = pipeline(
    prompt,
    do_sample=False,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
    max_length=8129
)
for seq in sequences:
    print("---"*20)
    print(f"Result: {seq['generated_text']}")

# # =============使用VLLM加速之后的推理方式，快很多=============
# from vllm import LLM, SamplingParams

# # Sample prompts.
# prompts = [
#     raw_input
# ]
# Create a sampling params object.
# sampling_params = SamplingParams(
#   presence_penalty=0.2,
#   frequency_penalty=0.2,
#   temperature=0.2,
#   top_p=0.9,
#   max_tokens=8192
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
