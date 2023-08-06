import os
from typing import List


def _can_add_file(file: str, exts: List[str], folder_out: List[str]):
    for ext in exts:
        if file.endswith(ext):
            return False
    splited = file.split(os.path.sep)
    for dirr in splited:
        for fold in folder_out:
            if dirr == fold:
                return False
    return True


def get_all_files(
    folder_or_file_path: str,
    folder_exclude: List[str],
    file_ext_exclude: List[str],
) -> List[str]:
    if os.path.isfile(folder_or_file_path):
        return [folder_or_file_path]
    if os.path.isdir(folder_or_file_path):
        res = []
        for root, _, files in os.walk(folder_or_file_path):
            for file in files:
                if not _can_add_file(file, file_ext_exclude, folder_exclude):
                    continue
                res.append(os.path.join(root, file))
        return res
    raise os.error(f"Invalid path: {folder_or_file_path}")
