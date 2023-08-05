from typing import Optional
from dataclasses import dataclass

from zetsubou.project.model.kind import ETargetKind
from zetsubou.project.model.runtime_library import ERuntimeLibrary


@dataclass
class TargetFilter():
    config_string: str = '*'
    kind: Optional[ETargetKind] = None
    runtime_library: Optional[ERuntimeLibrary] = None
