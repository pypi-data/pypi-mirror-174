from enum import Enum


class ETargetKind(Enum):
    INVALID = 0x0
    EXECUTABLE = 0x1
    STATIC_LIBRARY = 0x2
    DYNAMIC_LIBRARY = 0x3
    OBJECT_LIBRARY = 0x4
    HEADER_ONLY = 0x5
    IMPORTED_TARGET = 0x6


def is_target_kind_linkable(kind : ETargetKind) -> bool:
    if kind in [ ETargetKind.HEADER_ONLY, ETargetKind.IMPORTED_TARGET ]:
        return False
    return True


def is_target_library(kind : ETargetKind) -> bool:
    return kind != ETargetKind.EXECUTABLE
