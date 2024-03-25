# 运行此文件前需要运行一下：/Users/zandaoguang/Desktop/Intern/huawei/codes/scripts/clean_repos.ipynb

# Copyright (c) Huawei Cloud.
# Licensed under the MIT license.
import json
import sys
import os
import re
import ipdb
import shutil

import isort
import autopep8
import black

import logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class RepoCleaner():
    """
    Strategies to clean a repository.
    """

    @staticmethod
    def remove_copy_right(python_file_content):
        """
        Clean the given python file by removing copy right.
        """
        # Remove copy right in the beginning of the file.
        copyright_regex = r"^\s*#.*(?:\n\s*#.*)*"
        cleaned_content = re.sub(copyright_regex, '', python_file_content, count=1, flags=re.MULTILINE)

        return cleaned_content.strip()
    
    @staticmethod
    def remove_empty_folders(path):
        is_deleted = False

        if not os.path.isdir(path):
            return is_deleted
        
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                if RepoCleaner.remove_empty_folders(full_path):
                    is_deleted = True

        if not os.listdir(path):
            logging.info(f"Removing empty folder: {path}")
            os.rmdir(path)
            is_deleted = True

        return is_deleted
    
    @staticmethod
    def delete_md(path):
        """
        Delete all the ".md" files in a directory except the "README.md" file.
        """
        remained_path = os.path.join(path, "README.md")
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".md"):
                    # os.remove(os.path.join(root, file))
                    this_md_path = os.path.join(root, file)
                    if this_md_path == remained_path:
                        continue
                    os.system(f"rm -rf {this_md_path}")

def not_contains_py_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                return False
    return True

def list_all_paths(repo_path):
    """
    Get all file or folder paths in a directory
    """
    all_repo_paths = []
    for root, dirs, files in os.walk(repo_path):
        for dir in dirs:
            if dir.startswith('.'):
                continue
            all_repo_paths.append(os.path.join(root, dir))
        for file in files:
            if file.startswith('.'):
                continue
            all_repo_paths.append(os.path.join(root, file))

    return all_repo_paths

def mkdir_folder_for_file(file_path):
    """
    Create folder for a file if not exists.
    """
    folder_path = os.path.dirname(file_path)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Running clean script for given repository.')
    parser.add_argument('--base_path', type=str, help='Path to repository.')
    parser.add_argument('--new_base_path', type=str, help='Cleaned repository path.')
    parser.add_argument('--repo_names', type=str, help='Repository names.')
    
    args = parser.parse_args()

    repo_names = args.repo_names.split(',')
    for repo_name in repo_names:
        repo_path = os.path.join(args.base_path, repo_name)
        new_repo_path = os.path.join(args.new_base_path, repo_name)
        logging.info(f"")
        
        # reset new_repo_path
        # if os.path.exists(new_repo_path):
        #     os.system(f"rm -rf {new_repo_path}")

        all_repo_paths = list_all_paths(repo_path)
        logging.info(f"total {len(all_repo_paths)} files in {repo_path}, cleaning...")
        
        for old_path in all_repo_paths:
            new_path = old_path.replace(args.base_path, args.new_base_path)
            
            assert "test" not in repo_name and "log" not in repo_name
            if "test" in new_path or "log" in new_path:
                continue

            if os.path.isdir(old_path): # folder
                flag = False
                for folder in os.path.dirname(new_path).split("/"):
                    if folder.startswith('.') and "." != folder:
                        flag = True
                        break
                if flag:
                    continue
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
            else: # file
                # if os.path.dirname(new_path).
                flag = False
                for folder in os.path.dirname(new_path).split("/"):
                    if folder.startswith('.') and "." != folder:
                        flag = True
                        break
                if flag:
                    continue
                if not os.path.exists(os.path.dirname(new_path)):
                    os.makedirs(os.path.dirname(new_path))
                if new_path.endswith('.py'):
                    with open(old_path, 'r') as f:
                        python_file_content = f.read()
                    cleaned_python_file_content = RepoCleaner.remove_copy_right(python_file_content)
                    try:
                        sorted_code = isort.code(cleaned_python_file_content)
                        # beatified_code = autopep8.fix_code(sorted_code) # using `autopep8`
                    except:
                        continue
                    try:
                        beatified_code = black.format_str(sorted_code, mode=black.FileMode()) # using `black`
                    except:
                        beatified_code = sorted_code
                    with open(new_path, 'w+') as f:
                        f.write(beatified_code)
                elif "README.md" in new_path:
                    if os.path.exists(new_path):
                        continue
                    shutil.copyfile(old_path, new_path)
                elif "requirements.txt" in new_path:
                    shutil.copyfile(old_path, new_path)
                elif new_path.endswith('.sh') or new_path.endswith('html'):
                    shutil.copyfile(old_path, new_path)
                else:
                    # with open(new_path, 'w+') as f:
                    #     f.write('')
                    pass

        logging.info(f"finished cleaning {repo_path}.")
        logging.info(f"clean done!")

        # Delete all the ".md" files in a directory except the "README.md" file.
        RepoCleaner.delete_md(new_repo_path)
        logging.info(f"delete md done!")
        
        # Delete all empty folders in new_repo_path
        RepoCleaner.remove_empty_folders(new_repo_path)
        logging.info(f"remove empty folders done!")

        if not_contains_py_files(new_repo_path):
            logging.info(f"no py files in {new_repo_path}, removing...")
            os.system(f"rm -rf {new_repo_path}")
            logging.info(f"remove done!")