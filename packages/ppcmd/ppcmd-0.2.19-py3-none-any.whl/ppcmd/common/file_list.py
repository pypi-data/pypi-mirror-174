import os
import os.path
from enum import Enum
from glob import glob


def last_modified_file_in__(directory: os.path, ext: str):
    files = file_list_in__(directory, ext, FileSortType.UPDATE_TIME, reverse_order=True)
    if len(files) > 0:
        return files[0]

    return ''


class FileSortType(Enum):
    NAME = 1
    UPDATE_TIME = 2


def file_list_in__(directory: os.path, ext: str,
                   sort_type: FileSortType = FileSortType.NAME,
                   reverse_order: bool = False):
    files = glob(directory + f'/**/*.{ext}', recursive=True)

    if sort_type == FileSortType.NAME:
        return sorted(files, key=os.path.basename, reverse=reverse_order)
    if sort_type == FileSortType.UPDATE_TIME:
        return sorted(files, key=os.path.getmtime, reverse=reverse_order)

    raise RuntimeError('invalid file sort type')
