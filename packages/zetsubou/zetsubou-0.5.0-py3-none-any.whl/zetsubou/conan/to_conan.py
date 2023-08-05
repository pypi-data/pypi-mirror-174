from zetsubou.commands.base_command import CommandContext
from typing import List


def platform_to_conan(context: CommandContext, plat : str) -> List[str]:
    return [
        '-s', f'os={plat}'
    ]


def toolchain_to_conan(context: CommandContext, toolchain_name: str) -> List[str]:
    toolchain = context.project_template.find_toolchain(toolchain_name)
    if toolchain is not None:

        arch = {
            'x86' : 'x86',
            'x64' : 'x86_64'
        }.get(toolchain.arch)

        compiler = {
            'MSVC'  : 'Visual Studio',
            'CLANG' : 'lvvm',
            'GCC'   : 'gcc' 
        }.get(toolchain.CompilerFamily.name)

        version_dot = toolchain.ide_version.find('.')

        return [
            '-s', f'arch={arch}',
            '-s', f'compiler={compiler}',
            '-s', f'compiler.toolset={toolchain.Toolset}',
            '-s', f'compiler.version={toolchain.ide_version[0:version_dot]}',
        ]
    return []


def config_base_to_conan(context: CommandContext, cfg: str) -> List[str]:
    config = context.project_template.find_config(cfg)
    if config is not None:

        build_type = {
            'DEBUG' : 'Debug',
            'RELEASE' : 'Release',
            'RELEASE_WITH_DEBUG_INFO' : 'RelWithDebInfo'
        }.get(config.base_configuration.name)

        runtime_library = {
            'DYNAMIC_DEBUG'   : 'MDd',
            'DYNAMIC_RELEASE' : 'MD',
            'STATIC_DEBUG'    : 'MTd',
            'STATIC_RELEASE'  : 'MT',
        }.get(config.runtime_library.name)

        return [
            '-s', f'build_type={build_type}',
            '-s', f'compiler.runtime={runtime_library}'
        ]
    return []
