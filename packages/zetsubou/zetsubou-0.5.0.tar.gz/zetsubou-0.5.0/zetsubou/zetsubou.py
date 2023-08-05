from __future__ import absolute_import
import os
import sys
import time

from fs.osfs import OSFS
from zetsubou.commands.base_command import CommandContext, Command
from zetsubou.commands.command_registry import get_all_commands

from zetsubou.logo import print_logo
from zetsubou.project.runtime.project_loader import ProjectError
from zetsubou.utils import logger
from zetsubou.utils.cmd_arguments import parse_arguments
from zetsubou.utils.common import fix_path
from zetsubou.utils.error_codes import EErrorCode, ReturnErrorcode
from zetsubou._version import get_author_desc

def main() -> int:
    desc = f'FASTbuild project generator for the helpless\n{get_author_desc()}'
    progname = 'zetsubou'
    start_time = time.time()
    logger.Initialize()

    try:
        # populate command list
        command_registry = get_all_commands()

        # parse cmd arguments
        zet_args = parse_arguments(sys.argv[1:], progname, desc, command_registry)

        if not zet_args.nologo and not zet_args.silent:
            print_logo(desc)

        if zet_args.silent:
            logger.SetLogLevel(logger.ELogLevel.Silent)
        elif zet_args.verbose:
            logger.SetLogLevel(logger.ELogLevel.Verbose)

        has_project_context = hasattr(zet_args, 'project')

        fs_root = os.path.dirname(os.path.normpath(os.path.join(os.getcwd(), zet_args.project))) if has_project_context else os.getcwd()
        project_file = os.path.basename(zet_args.project) if has_project_context else None

        command_context = CommandContext(
            fs_root = fix_path(fs_root),
            command_args = zet_args,
            project_file = project_file,
            project_fs = OSFS(fs_root)
        )

        logger.Info(f"Current working directory - '{os.getcwd()}'")
        logger.Info(f"Project working directory - '{fs_root}'")

        cmd = Command.get_command_by_name(zet_args.command)
        cmd.Execute(command_context)

        end_time = time.time()

        if not zet_args.silent:
            print(f'\nFinished in {end_time - start_time:.2f} sec')

        return 0

    except ReturnErrorcode as errcode:
        logger.ReturnCode(errcode.error_code)
        return errcode.error_code.value

    except ProjectError as proj_error:
        logger.Error(proj_error)
        logger.ReturnCode(EErrorCode.UNKNOWN_ERROR)
        return 666

    except Exception as error:
        logger.Exception(error)
        return 666

# Process draft:
# OS required:
# - python 3.x
# - conan
# - vstudio
# Install process:
# - venc setup
#   - conan installs dev dependencies:
#     - zetsubou
#     - fastbuild
# - call vswhere
# - process yml
# - generate files
# zet install
# installing dev virtual environment...
# zet create - emit template for something
# zet install - install virtual environment
# zet config - emit fastbuild files
# zet build - call build on fastbuild
# zet clean - clean generated files
# zet list - list all commands
# zet clean install config build