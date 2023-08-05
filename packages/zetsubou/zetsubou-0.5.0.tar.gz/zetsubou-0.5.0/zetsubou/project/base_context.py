from dataclasses import dataclass
from fs.base import FS


@dataclass
class BaseContext:
    fs_root: str = ''
    fs_venv: str = ''
    project_fs: FS = ''
    project_file: str = ''
