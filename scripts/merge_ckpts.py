import subprocess
import os
import glob
import ipdb

def merge_files(file_path, model_prefix, output_filename):
    """
    使用cat命令合并分割的文件。

    Args:
    - model_prefix: 分割文件的前缀模式。
    - output_filename: 合并后文件的名称。
    """
    files = glob.glob(os.path.join(file_path, model_prefix) + "*")
    files.sort()
    
    # 合并files
    cat_command = ['cat'] + files
    with open(os.path.join(file_path, output_filename), 'wb+') as outfile:
        subprocess.run(cat_command, stdout=outfile)

    # 删除files
    rm_command = ['rm'] + files
    subprocess.run(rm_command)

def main():
    file_path = "/Users/zandaoguang/Desktop/CodeLlama-7b-Instruct"
    models = [
        ("pytorch_model-00001-of-00003.bin.part", "pytorch_model-00001-of-00003.bin"),
        ("pytorch_model-00002-of-00003.bin.part", "pytorch_model-00002-of-00003.bin"),
        ("pytorch_model-00003-of-00003.bin.part", "pytorch_model-00003-of-00003.bin"),
    ]
    
    for model_prefix, output_filename in models:
        print(f"Merging files for {model_prefix} into {output_filename}")
        merge_files(file_path, model_prefix, output_filename)
        print(f"Merged files for {model_prefix} into {output_filename}")

if __name__ == "__main__":
    main()
