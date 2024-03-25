import json
import os

saved_name = "codes_train_data_v11_24.03.08.json"
max_lens_for_repo = 50
code_data_size = 2000
nl_data_size = 2000

# # Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM
# tokenizer = AutoTokenizer.from_pretrained("/Users/zandaoguang/Desktop/CodeLlama-7b-Instruct")

# def cal_tokens(text):
#     inputs = tokenizer(text)
#     input_ids = inputs["input_ids"]
#     return len(input_ids)

path = "/Users/zandaoguang/Desktop/Intern/huawei/codes/outputs"
new_data = []
over_num = 0
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            with open(file_path, "r") as file:
                data = json.load(file)
                filted_data = []
                for item in data:
                    # this_tokens = cal_tokens(item["instruction"]+item["output"])
                    # print(this_tokens)
                    words_len = len((item["instruction"]+item["output"]).split(" "))
                    if words_len > 10000:
                        over_num += 1
                        continue
                    # if this_tokens > max_sizes:
                    #     max_sizes = this_tokens
                    filted_data.append(item)

                import random
                random.shuffle(filted_data)

                new_data.extend(filted_data[:max_lens_for_repo])               

print(f"over: {over_num}")
print(f"saved: {len(new_data)}")

saved_path = f"/Users/zandaoguang/Desktop/Intern/huawei/codes/training_data/{saved_name}"

with open(saved_path, "w+") as file:
    json.dump(new_data, file, indent=4)

print("done!")