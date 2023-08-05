from sys import platform
from typing import List

from zetsubou.project.model.platform import EArch, Platform
from zetsubou.project.model.toolchain import Toolchain
from zetsubou.utils.common import is_in_enum
from zetsubou.utils.error import ProjectError


def discover_toolchain_list() -> List[Toolchain] :
    if platform == 'win32':
        from zetsubou.system.windows import windows
        return windows.discover_toolchain_list()
    else:
        raise EnvironmentError(f'Sorry, platform \"{platform}\" is not currently supported!')


def filter_toolchains_by_arch(toolchain:Toolchain, platforms:List[Platform]):
    for plat in platforms:
        if not is_in_enum(toolchain.arch, EArch):
            raise ProjectError(f"Unknown arch '{toolchain.arch}' for toolchain '{toolchain.name}'")

        if EArch[toolchain.arch] == plat.target_arch:
            return True

    return False


def filter_toolchains_by_conan(toolchain:Toolchain, conan_settings):
    try:
        if toolchain.Toolset in conan_settings['compiler']['Visual Studio']['toolset']:
            return True
    except Exception:
        return False
    return False
