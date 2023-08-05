from typing import List
from sys import platform


def is_in_enum(value: str, enum_class):
    return value in enum_class.__members__


# Find more appropriate way to do this...
def fix_path(path : str):
    path = path.replace('\\\\', '/')
    path = path.replace('\\', '/')
    return path


def fix_path_win32(path : str):
    path = path.replace('/', '\\')
    return path


def fix_path_os(path : str):
    posix_path = fix_path(path)
    if platform == 'win32':
        return fix_path_win32(posix_path)
    return posix_path


def null_or_empty(txt : str):
    return txt is None or txt == ''


def split(pred, collection):
    a = []
    b = []
    for element in collection:
        if pred(element):
            a.append(element)
        else:
            b.append(element)
    return a, b


def join_unique(lists : List[List[str]]):
    unique = list()
    for entry in lists:
        unique.extend(j for j in entry if j not in unique)
    return unique


def list_to_string(lists : List[str]):
    return f" {' '.join(lists)}"
