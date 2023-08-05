from enum import Enum


class ERuntimeLibrary(Enum):
    DYNAMIC_DEBUG   = 0,
    DYNAMIC_RELEASE = 1,
    STATIC_DEBUG    = 2,
    STATIC_RELEASE  = 3
