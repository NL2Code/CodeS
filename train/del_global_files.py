import os
import shutil
import time

def delete_folders_with_prefix(root_dir, prefix):
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            if dirname.startswith(prefix):
                folder_to_delete = os.path.join(dirpath, dirname)
                print(f"Deleting {folder_to_delete} ...")
                shutil.rmtree(folder_to_delete)
                print("Done!")

root_path = "/dev/shm/"

while True:
    delete_folders_with_prefix(root_path, "global_step")
    time.sleep(500)
    print("Start checking")
