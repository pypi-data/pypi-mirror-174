import winreg
import os, json, ctypes
from typing import List, Optional, Any
from dataclasses import dataclass

from zetsubou.project.model.toolchain import ECompilerFamily, Toolchain
from zetsubou.system.windows import vswhere
from zetsubou.utils import logger


def is_current_host(host: str) -> bool:
    is_64bit : bool = ctypes.sizeof(ctypes.c_void_p) == 8
    # x64
    if host.endswith('64') and is_64bit:
        return True
    # x86 (32-bit)
    if not is_64bit:
        return True
    return False


def get_subdirs(dir: str):
    return [f.name for f in os.scandir(dir) if f.is_dir]


@dataclass
class Toolset:
    full_path: str
    identifier: str


def find_toolsets(msvc_path : str) -> List[Toolset]:
    toolsets = []
    search_subpath = 'Msbuild\\Microsoft\\VC'
    search_path = os.path.join(msvc_path, search_subpath)
    if os.path.exists(search_path):
        for root, _, files in os.walk(search_path):
            if 'Toolset.props' in files:
                toolsets.append(Toolset(full_path=root, identifier=os.path.basename(root)))

    return toolsets


# Filters out legacy versions of toolsets, leaving only the latest one
def filter_legacy_toolsets(msvc_path : str, toolsets: List[Toolset]) -> List[Toolset]:
    msvc_path = os.path.join(msvc_path, 'Msbuild\\Microsoft\\VC\\')
    selected_version = ''
    result = []

    # Filter out legacy toolsets
    for tool in toolsets:
        if tool.full_path.startswith(msvc_path):
            tmp_path = tool.full_path[len(msvc_path):]
            first_slash_idx = tmp_path.find('\\')
            tmp_path = tmp_path[:first_slash_idx]
            if tmp_path > selected_version:
                selected_version = tmp_path
    for tool in toolsets:
        if selected_version in tool.full_path:
            result.append(tool)

    return result


def get_registry_key(storage : str, key : str, entry : str) -> Optional[Any]:
    try:
        hkey = winreg.OpenKey(storage, key)
    except:
        return None
    else:
        try:
            value, _ = winreg.QueryValueEx(hkey, entry)
            return value
        except:
            return None
        finally:
            winreg.CloseKey(hkey)


@dataclass
class WindowsSDKPaths:
    version : str
    base_path : str
    include : str
    lib : str
    bin : str


def discover_win10_sdk():
    storages = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]
    key_paths = ['SOFTWARE\\Wow6432Node', 'SOFTWARE']

    for storage in storages:
        for key in key_paths:

            key_path = f'{key}\\Microsoft\\Microsoft SDKs\\Windows\\v10.0'
            install_dir = get_registry_key(storage, key_path, 'InstallationFolder')

            if install_dir and os.path.isdir(install_dir):
                include_dir = os.path.join(install_dir, 'include')

                sdk_versions = os.listdir(include_dir)
                latest_sdk = max(sdk_versions)

                if os.path.isdir(os.path.join(include_dir, latest_sdk)) and latest_sdk.startswith('10.'):
                    windows_h = os.path.join(include_dir, latest_sdk, 'um', 'Windows.h')
                    if os.path.isfile(windows_h):
                        sdk = WindowsSDKPaths(
                            version=latest_sdk,
                            base_path=install_dir,
                            include=os.path.join(install_dir, 'Include', latest_sdk),
                            lib=os.path.join(install_dir, 'Lib', latest_sdk),
                            bin=os.path.join(install_dir, 'bin', latest_sdk),
                        )
                        return sdk
    return None


def discover_vswhere() -> List[Toolchain]:
    toolchains : List[Toolchain] = []
    vswhere_path = None

    try:
        vswhere_path = vswhere.find_vswhere()
    except Exception:
        pass

    if vswhere_path is None:
        logger.Warning("Unable to find vswhere executable, VS toolchains not discovered")
        return []

    vs_instances = json.loads(vswhere.call_vswhere(vswhere_path))
    if vs_instances is None:
        logger.Warning("vswhere found no VS installations")
        return []

    default_vc_path = 'VC\\Tools\\MSVC'
    default_bin_path = 'bin'
    default_lib_path = 'lib'
    default_include_paths = ['include', 'atlmfc\\include']
    default_compiler_msvc = 'cl.exe'
    default_linker_msvc = 'link.exe'
    default_librarian_msvc = 'lib.exe'

    additional_include_dirs = [
        'VC\\Auxiliary\\VS\\include',
        'VC\\Auxiliary\\VS\\UnitTest\\include'
    ]

    default_compiler_options = '/c "%1" /Fo"%2" '
    default_linker_options = '/OUT:"%2" "%1" '
    default_librarian_options = '/OUT:"%2" "%1" '

    default_extra_files = [
        'c1.dll',
        'c2.dll',
        'c1xx.dll',
        '1033\\clui.dll',
        'msobj140.dll',
        'mspdb140.dll',
        'mspdbsrv.exe',
        'mspdbcore.dll',
        'mspft140.dll',
        'msvcp140.dll',
        'vcruntime140.dll',
        'vccorlib140.dll'
    ]

    default_link_libraries = [
        'kernel32'
        'user32'
        'gdi32'
        'winspool'
        'comdlg32'
        'advapi32'
        'shell32'
        'ole32'
        'oleaut32'
        'uuid'
        'odbc32'
        'odbccp32'
        'delayimp'
    ]

    for vs_itr in vs_instances:
        installation_path = vs_itr['installationPath']
        vs_ide_version = vs_itr['installationVersion']
        vc_tools = os.path.join(installation_path, default_vc_path)
        vs_version = vs_itr['catalog']['productLineVersion']

        # There is a thing I cannot find documentation about
        # Seems the Clang toolset exists in two versions per visual studio installation
        #   egx. 2022 has v170 and v160 folders with Clang
        #    and 2019 has v160 and v150
        # We don't want th
        toolsets = find_toolsets(installation_path)
        toolsets = filter_legacy_toolsets(installation_path, toolsets)

        if os.path.exists(vc_tools):
            vc_versions = get_subdirs(vc_tools)

            vc_ver = max(vc_versions)

            # for vc_ver in vc_versions:
            vc_ver_basepath = os.path.join(vc_tools, vc_ver)
            vc_ver_binpath = os.path.join(vc_ver_basepath, default_bin_path)
            vc_ver_libpath = os.path.join(vc_ver_basepath, default_lib_path)

            for host in get_subdirs(vc_ver_binpath):
                if is_current_host(host):
                    for arch in get_subdirs(os.path.join(vc_ver_binpath, host)):

                        msvc_name = vc_ver.replace('.','_')
                        arch_bin_fullpath = os.path.join(vc_ver_binpath, host, arch)
                        arch_lib_fullpath = os.path.join(vc_ver_libpath, arch)

                        visited_toolsets = set()

                        for entry in toolsets:
                            if arch in entry.full_path and entry.identifier not in visited_toolsets:
                                visited_toolsets.add(entry.identifier)
                                toolchain_name = f'MSVC_{arch}_vs{vs_version}_v{msvc_name}_{entry.identifier}'

                                includes = []
                                includes += [ os.path.join(vc_ver_basepath, inc) for inc in default_include_paths ]
                                includes += [ os.path.join(installation_path, inc) for inc in additional_include_dirs ]

                                machine_linker_options = f'/MACHINE:{arch} '

                                compiler = Toolchain(
                                    name=toolchain_name,
                                    arch=arch,

                                    version=vc_ver,
                                    ide_version=vs_ide_version,
                                    vs_install_path=installation_path,
                                    vs_msvc_path=vc_ver_binpath,

                                    Toolset=entry.identifier,

                                    Compiler=os.path.join(arch_bin_fullpath, default_compiler_msvc),
                                    CompilerFamily=ECompilerFamily.MSVC,
                                    CompilerOptions=default_compiler_options,

                                    Linker=os.path.join(arch_bin_fullpath, default_linker_msvc),
                                    LinkerOptions=default_linker_options + machine_linker_options,
                                    LinkerPaths=[
                                        arch_lib_fullpath,
                                        arch_bin_fullpath,
                                    ],

                                    Librarian=os.path.join(arch_bin_fullpath, default_librarian_msvc),
                                    LibrarianOptions=default_librarian_options,

                                    ExtraFiles = default_extra_files,

                                    RequiredFiles=[],
                                    IncludeDirectories=includes,
                                    Defines=[]
                                )
                                toolchains.append(compiler)

    return toolchains


def discover_clang() -> List[Toolchain]:
    return []


def discover_toolchain_list() -> List[Toolchain] :
    toolchains : List[Toolchain] = []
    toolchains += discover_vswhere()
    toolchains += discover_clang()

    win10_sdk = discover_win10_sdk()

    if win10_sdk is not None:
        for toolchain in toolchains:
            if toolchain.CompilerFamily == ECompilerFamily.MSVC:
                toolchain.LinkerPaths.append(f'{win10_sdk.lib}\\um\\{toolchain.arch.lower()}')
                toolchain.LinkerPaths.append(f'{win10_sdk.lib}\\ucrt\\{toolchain.arch.lower()}')
                toolchain.IncludeDirectories.append(f'{win10_sdk.include}\\shared')
                toolchain.IncludeDirectories.append(f'{win10_sdk.include}\\um')
                toolchain.IncludeDirectories.append(f'{win10_sdk.include}\\ucrt')

    return toolchains
