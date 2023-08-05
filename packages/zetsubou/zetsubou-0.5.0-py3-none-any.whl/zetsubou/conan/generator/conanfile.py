from conans.model import Generator
from conans import ConanFile
import os


def emit_list(lst):
    return '\n       - '.join(lst)


def emit_property(out, prop, tmpl):
    if prop is not None and len(prop) > 0:
        out.append(tmpl.format(data = emit_list(prop)))


def fix_no_ext(libs, paths):
    results = []
    for path in paths:
        for _, _, filenames in os.walk(path):
            for file in filenames:
                for lib in libs:
                    if file.find(lib) != -1:
                        results.append(os.path.basename(file))
    return results


class zetsubou_multi(Generator):
    @property
    def filename(self):
        pass

    @property
    def content(self):
        result = {}

        for dep_name, dep_cpp_info in self.deps_build_info.dependencies:
            sections = []
            emit_property(sections, dep_cpp_info.include_paths,
                '    includes:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, dep_cpp_info.defines,
                '    defines:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, dep_cpp_info.cppflags,
                '    compiler_flags:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, fix_no_ext(dep_cpp_info.libs, dep_cpp_info.lib_paths),
                '    link_libraries:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, dep_cpp_info.lib_paths,
                '    linker_paths:\n'
                '       interface:\n'
                '       - {data}\n')

            emit_property(sections, dep_cpp_info.sharedlinkflags + dep_cpp_info.exelinkflags,
                '    linker_flags:\n'
                '       interface:\n'
                '       - {data}\n')

            dep_name = dep_name.replace("-", "_")
            result[f'{dep_name}.part.yml'] = ''.join(sections)

        # result['conan_multi.txt'] = '\n'.join([ name for name, _ in self.deps_build_info.dependencies ])

        return result


class ZetsubouGeneratorPackage(ConanFile):
    name = "zetsubougen"
    version = "0.5.0"
    url = "https://github.com/..."
    license = "MIT"
    description = 'Zetsubou yml files generator'

    def build(self):
        pass

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
