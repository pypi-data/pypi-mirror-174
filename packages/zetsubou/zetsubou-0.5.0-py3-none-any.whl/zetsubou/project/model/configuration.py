from typing import List, Optional
from dataclasses import dataclass, field
from enum import Enum

from zetsubou.project.model.filter import TargetFilter
from zetsubou.project.model.runtime_library import ERuntimeLibrary
from zetsubou.project.model.target import TargetData
from bentoudev.dataclass.base import loaded_from_file


# For compatibility purposes, custom configurations must fallback to one of the default ones, to communicate with VS and Conan
class EBaseConfiguration(Enum):
    DEBUG = 0
    RELEASE = 1
    RELEASE_WITH_DEBUG_INFO = 2


@dataclass
class ConfigurationData(TargetData):
    filter: TargetFilter = TargetFilter()


@dataclass
@loaded_from_file
class Configuration(TargetData):
    configuration: str = None
    base_configuration: EBaseConfiguration = None
    filters: List[ConfigurationData] = field(default_factory=list)
    runtime_library: ERuntimeLibrary = ERuntimeLibrary.DYNAMIC_RELEASE
