from argparse import ArgumentParser
import os
import venv
from zetsubou.commands.base_command import Command, CommandContext, execute_stage
from zetsubou.conan.dependencies import ConanDependencies
from zetsubou.utils import logger
from zetsubou.utils.error_codes import EErrorCode
from zetsubou.utils.yaml_tools import to_yaml
from zetsubou.conan.conan import check_conan_present, call_conan
from zetsubou.conan.to_conan import toolchain_to_conan, platform_to_conan, config_base_to_conan


class Install(Command):
    @property
    def name(self):
        return 'install'

    @property
    def desc(self):
        return 'Setup virtual environment, install build dependencies.'

    @property
    def help(self):
        return self.desc

    def ParseArgs(self, arg_parser: ArgumentParser):
        pass

    def OnExecute(self, context: CommandContext):
        context.project_fs.makedirs('build/venv', recreate=True)

        if context.project_template.project.conan is not None and check_conan_present():
            self.generate_conan_environment(context)
        else:
            self.generate_empty_environment(context)

    def generate_empty_environment(self, context: CommandContext):
        env_builder = venv.EnvBuilder()
        venv_fs = context.project_fs.geturl('build/venv', purpose='fs')
        venv_fs = venv_fs.split('osfs://')[1]
        env_builder.create(venv_fs)
        logger.Info('Created new virtual environment')

    def generate_conan_environment(self, context: CommandContext):
        CONAN_OUT_PATH = 'build/conan'
        conan_build_tools = context.project_template.project.conan.build_tools
        if conan_build_tools is not None:
            conan_build_tools = context.to_out_path(conan_build_tools)
            execute_stage(lambda: call_conan(['install', conan_build_tools, '-g=virtualenv'], context.to_out_path('build/venv')),
                        'Conan build tools installed',
                        EErrorCode.UNABLE_TO_INSTALL_CONAN_BUILD_TOOLS)

        conan_deps = context.project_template.project.conan.dependencies
        if conan_deps is None:
            return

        conan_deps = context.to_out_path(conan_deps)

        for config_variant in context.config_matrix.variants:
            logger.Verbose(f"Installing configuration '{config_variant.config_string}'")

            toolchain = config_variant.get_slot('toolchain')
            platform = config_variant.get_slot('platform')
            config = config_variant.get_slot('configuration')

            conan_settings = []
            conan_settings.extend(platform_to_conan(context, platform))
            conan_settings.extend(toolchain_to_conan(context, toolchain))
            conan_settings.extend(config_base_to_conan(context, config))

            conan_config_out_path = f'{CONAN_OUT_PATH}/{config_variant.config_string.replace("-", ".")}'
            context.project_fs.makedirs(conan_config_out_path, recreate=True)

            execute_stage(lambda: call_conan(
                        ['install', conan_deps, f'--build={context.project_template.project.conan.build}'] + conan_settings,
                        context.to_out_path(conan_config_out_path)),
                        f"Conan configuration '{config_variant.config_string}' installed",
                        EErrorCode.UNABLE_TO_INSTALL_CONAN_DEPENDENCIES)

        dep_matrix = {}
        for path in context.project_fs.walk.files(path=CONAN_OUT_PATH, filter=['*.part.yml']):
            dep_name = os.path.basename(path).rsplit('.')[0]
            config_string = (os.path.basename(os.path.dirname(path))).replace('.', '-')

            if dep_name not in dep_matrix:
                dep_matrix[dep_name] = [
                    f'target: {dep_name}\n'
                    'config:\n'
                    '  kind: IMPORTED_TARGET\n'
                    'filters:\n'
                ]

            dep_target = dep_matrix[dep_name]

            with context.project_fs.open(path, mode='r') as part_file:
                dep_target.append(f"  - filter:\n       config_string: '{config_string}'\n")
                dep_target.append(part_file.read())

            dep_matrix[dep_name] = dep_target

        # Merge targets configurations into one file
        out_ymls = []
        for dep_name, dep_content in dep_matrix.items():
            out_yml_path = f'{CONAN_OUT_PATH}/{dep_name}.yml'
            out_ymls.append(out_yml_path)

            with context.project_fs.open(out_yml_path, mode='w') as out_file:
                out_file.write(''.join(dep_content))

        # Merge targets into one file
        if len(out_ymls) > 0:

            with context.project_fs.open('build/conan_deps.yml', mode='w') as out_file:
                conan_deps = ConanDependencies(conanfile=conan_deps, targets=out_ymls)
                out_file.write(to_yaml(conan_deps))

            context.conan.yml_files = out_ymls
