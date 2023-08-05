from argparse import ArgumentParser
from typing import List
from zetsubou.commands.base_command import Command
from zetsubou.commands.clean import Clean
from zetsubou.commands.generate import Generate
from zetsubou.commands.regen import Regen
from zetsubou.commands.install import Install
from zetsubou.commands.create import Create
from zetsubou.commands.build import Build


def get_all_commands() -> List[Command]:
    if not Command.is_initialized():
        Command.initialize_command_instances([
            Clean(),
            Install(),
            Generate(),
            Regen(),
            Create(),
            Build(),
        ])

    return Command.get_commands()
