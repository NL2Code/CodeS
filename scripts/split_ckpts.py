import subprocess
import os

def split_file(file_path, number_of_parts=6):
    """
    分割指定文件为多个小文件，并保留特定的命名约定。

    Args:
    - file_path: 要分割的文件路径。
    - number_of_parts: 要分割成的文件数。
    """
    # 确保文件存在
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return
    
    # 获取文件大小
    file_size = os.path.getsize(file_path)
    # 计算每个分割文件应有的大致大小
    size_per_file = (file_size // number_of_parts) + 100

    prefix = file_path + ".part-"

    # 生成分割命令
    split_command = ['split', '-b', str(size_per_file), file_path, prefix]
    subprocess.run(split_command)

    # 删除原文件
    os.remove(file_path)

def main():
    file_path = "/Users/zandaoguang/Desktop/CodeLlama-7b-Instruct"
    files_to_split = ['pytorch_model-00001-of-00003.bin', 
                      'pytorch_model-00002-of-00003.bin', 
                      'pytorch_model-00003-of-00003.bin']
    
    for file in files_to_split:
        split_file(os.path.join(file_path, file))

if __name__ == "__main__":
    main()
