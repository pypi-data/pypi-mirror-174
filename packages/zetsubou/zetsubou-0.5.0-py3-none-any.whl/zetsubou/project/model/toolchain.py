from dataclasses import dataclass
from typing import List
from enum import Enum


class ECompilerFamily(Enum):
    MSVC   = 0,
    CLANG  = 1,
    GCC    = 2,
    CUSTOM = 3


@dataclass
class Toolchain:
    name: str
    version : str
    ide_version : str
    vs_install_path : str
    vs_msvc_path : str
    arch : str

    # Default include directories
    IncludeDirectories: List[str]

    # Additonal files copied with exe during distributed compilation
    RequiredFiles: List[str] 

    # (optional) Additional files (usually dlls) required by the compiler.
    ExtraFiles : List[str]

    # Default defines
    Defines: List[str]

    # Compiler executable
    Compiler: str

    # Compiler flags
    CompilerOptions : str

    # Compiler family
    CompilerFamily: ECompilerFamily

    # Linker executable
    Linker: str

    # Linker flags
    LinkerOptions : str

    # Paths with library files
    LinkerPaths : str

    # Librarian executable
    Librarian: str

    # Librarian flags
    LibrarianOptions : str

    # Toolset
    Toolset : str
