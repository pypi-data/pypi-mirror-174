from argparse import ArgumentParser
import time
import os

from dataclasses import dataclass, field
from typing import List, Optional, Any
from fs.base import FS

from bentoudev.dataclass.yaml_loader import LineLoader

from zetsubou.project.config_matrix import ConfigMatrix
from zetsubou.project.base_context import BaseContext
from zetsubou.project.model.target import Target
from zetsubou.project.model.toolchain import Toolchain
from zetsubou.project.runtime.resolve import ResolvedTarget
from zetsubou.project.runtime.project_loader import ProjectTemplate, load_project_from_file, resolve_venv
from zetsubou.project.config_matrix import create_config_matrix
from zetsubou.system import discover_toolchains
from zetsubou.utils import logger
from zetsubou.utils.common import null_or_empty, fix_path
from zetsubou.utils.error import ProjectError
from zetsubou.utils.error_codes import EErrorCode, ReturnErrorcode
from zetsubou.utils.yaml_tools import to_yaml


@dataclass
class Fastbuild:
    emit_fs : FS
    bff_dir : str
    bff_file : str


@dataclass
class Conan:
    yml_files: List[str] = field(default_factory=list)
    dependencies: List[Target] = field(default_factory=list)
    resolved_targets: List[ResolvedTarget] = field(default_factory=list)


@dataclass
class CommandContext(BaseContext):
    command_args: Any = None

    project_template: Optional[ProjectTemplate] = None
    toolchains: List[Toolchain] = field(default_factory=list)
    config_matrix: Optional[ConfigMatrix] = None
    resolved_targets: List[ResolvedTarget] = field(default_factory=list)
    fastbuild: Optional[Fastbuild] = None
    conan: Conan = Conan()


    def to_out_path(self, path : str):
        return os.path.join(self.fs_root, path)


    def resolve_venv(self):
        if null_or_empty(self.fs_venv):
            venv_path = execute_stage(lambda: resolve_venv(self.project_fs, self.project_template.project, self.fs_root),
                                        'Virtual environemnt found',
                                        EErrorCode.UNABLE_TO_FIND_VENV)

            logger.Info(f"Virtual environement - '{venv_path}'")
            self.fs_venv = fix_path(venv_path)


    def load_project(self):
        if self.project_template is None:

            logger.Command('load_project')

            # load and process project
            self.project_template = execute_stage(lambda: load_project_from_file(self.project_fs, self.fs_root, self.project_file),
                                        'Project loaded',
                                        EErrorCode.UNABLE_TO_LOAD_PROJECT)

            self.project_template.toolchains = self.toolchains

            # discover toolchains
            self.toolchains = execute_stage(discover_toolchains.discover_toolchain_list,
                                   'Toolchains discovered ({len})',
                                    EErrorCode.UNABLE_TO_DISCOVER_TOOLCHAIN)

            all_toolchains = self.toolchains
            num_all_toolchains = len(all_toolchains)

            # filter by platform
            self.toolchains = list(filter(lambda t: discover_toolchains.filter_toolchains_by_arch(t, self.project_template.platforms), self.toolchains))

            # filter by whatever is known to Conan
            user_dir = os.path.expanduser('~')
            conan_settings_path = os.path.join(user_dir, '.conan/settings.yml')

            if os.path.exists(conan_settings_path):
                with open(conan_settings_path, encoding='utf-8') as conan_settings_file:
                    loader = LineLoader(conan_settings_file.read())
                    loaded_yaml = loader.get_single_data()

                    # TODO: Windows: This depends on Windows and Visual Studio environment. Instead there should be other ways to filter toolchains!
                    self.toolchains = list(filter(lambda t: discover_toolchains.filter_toolchains_by_conan(t, loaded_yaml), self.toolchains))

                    num_toolchains = len(self.toolchains)

                    if num_toolchains == 0:
                        logger.Error(f"No suitable toolchains found! (Out of {num_all_toolchains} found in total)")

                        unsuitable_toolchains = to_yaml(all_toolchains)
                        logger.Warning(f"Available toolchains:\n{unsuitable_toolchains}")

                        toolkits = '\n'.join([ name for name in loaded_yaml['compiler']['Visual Studio']['toolset'] ])
                        logger.Warning(f"Available VS toolkits:\n{toolkits}")

                        raise ReturnErrorcode(EErrorCode.UNABLE_TO_DISCOVER_TOOLCHAIN)
                    else:
                        logger.Info(f"Found ({num_toolchains}) suitable toolchains.")

                        if self.command_args.verbose:
                            found_toolchains = to_yaml(self.toolchains)
                            logger.Verbose(f"Entries:\n{found_toolchains}")

            else:
                logger.Warning('Unable to filter toolchains by Conan settings!')

            self.project_template.toolchains = self.toolchains

            # create matrix of all options and their possible values
            self.config_matrix = execute_stage(lambda: create_config_matrix(self.project_template.project.config.config_string, self.project_template.slot_values()),
                                      'Config matrix created',
                                      EErrorCode.UNABLE_TO_CREATE_CONFIGURATIONS)


class Command:
    _commands : List['Command'] = []

    @staticmethod
    def is_initialized() -> bool:
        return len(Command._commands) > 0

    @staticmethod
    def initialize_command_instances(cmds : List['Command']):
        Command._commands = cmds

    @staticmethod
    def get_commands():
        return Command._commands

    @staticmethod
    def get_command_by_name(name:str):
        for c in Command._commands:
            if c.name == name:
                return c
        raise ValueError(f"Cannot find command with name '{name}'!")

    @staticmethod
    def get_command_instance(t):
        for c in Command._commands:
            if isinstance(c, t):
                return c
        raise ValueError(f"Cannot find instance of command '{t.__name__}'!")

    # User readable name
    @property
    def name(self):
        raise NotImplementedError()

    # Short information, displayed for --help
    @property
    def help(self):
        raise NotImplementedError()

    # Detailed information, displayed for COMMAND --help
    @property
    def desc(self):
        raise NotImplementedError()

    # Will require positional PROJECT argument
    # Will automatically load project before executing this command
    @property
    def needs_project_loaded(self):
        return True

    # Parses additional arguments that may be provided for this command
    def ParseArgs(self, arg_parser : ArgumentParser):
        raise NotImplementedError()

    def Execute(self, context : CommandContext):
        if self.needs_project_loaded:
            context.load_project()

        logger.Command(self.name)
        self.OnExecute(context)

    def OnExecute(self, context : CommandContext):
        raise NotImplementedError()


def execute_stage(func, succ_msg: str, err_code: EErrorCode):
    start_time = time.time()
    result = func()
    end_time = time.time()

    if result is not None and result is not False:
        if hasattr(result, '__len__'):
            succ_msg = succ_msg.format(len = len(result))

        logger.Success(f'{succ_msg} - {end_time - start_time:.2f}sec')
        return result
    else:
        raise ReturnErrorcode(err_code)
