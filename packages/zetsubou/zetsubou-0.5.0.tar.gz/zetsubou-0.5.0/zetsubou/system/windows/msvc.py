from zetsubou.project.model.platform import EArch
from zetsubou.utils.error import ProjectError

def arch_to_msvc_platform(arch : EArch):
    lookup = {
        EArch.x64 : 'x64',
        EArch.x86 : 'Win32'
    }

    if arch not in lookup:
        raise ProjectError(f"Arch '{arch}' is not supported for MSVC!")

    return lookup.get(arch)
