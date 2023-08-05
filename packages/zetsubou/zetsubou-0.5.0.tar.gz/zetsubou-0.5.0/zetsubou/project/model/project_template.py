from typing import List, Optional
from dataclasses import dataclass, field

from bentoudev.dataclass.base import loaded_from_file, track_source


@dataclass
@track_source
class ProjectConfig:
    verbose_build: bool = False
    platforms: List[str] = field(default_factory=list)
    configurations: List[str] = field(default_factory=list)
    # slots: Optional[List[str]] = field(default_factory=list)
    rules: Optional[List[str]] = field(default_factory=list)
    config_string: str = ''
    venv: Optional[str] = ''


@dataclass
class Option:
    name: str
    values: List[str]


@dataclass
class Conan:
    build_tools: Optional[str] = None
    dependencies: Optional[str] = None
    build: Optional[str] = 'missing'


@loaded_from_file
@dataclass
class Project:
    project: str
    config: ProjectConfig
    targets: List[str]
    conan: Optional[Conan] = None
    options: Optional[List[Option]] = field(default_factory=list)
