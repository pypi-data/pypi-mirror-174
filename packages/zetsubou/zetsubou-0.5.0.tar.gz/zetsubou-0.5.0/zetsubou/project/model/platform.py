from typing import List, Optional
from enum import Enum
from dataclasses import dataclass, field

from zetsubou.project.model.filter import TargetFilter
from zetsubou.project.model.target import TargetData
from bentoudev.dataclass.base import loaded_from_file


class EArch(Enum):
    x64 = 0
    x86 = 1


class ESystem(Enum):
    Windows = 0
    Linux = 1


@dataclass
class PlatformData(TargetData):
    filter: TargetFilter = TargetFilter()


@dataclass
@loaded_from_file
class Platform(TargetData):
    platform: str = None
    host_arch: EArch = None
    target_arch: EArch = None
    filters: Optional[List[PlatformData]] = field(default_factory=list)
