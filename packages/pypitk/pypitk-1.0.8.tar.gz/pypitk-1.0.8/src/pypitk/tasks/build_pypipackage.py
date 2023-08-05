import osiotk as os
from ..objects import PYPIPackage
from .. import init as _init
from .. import constants as _constants


def build_package(__package: PYPIPackage):
    def __iter_package_path_content(__package: PYPIPackage):
        for key in _constants.FILENAMES_PACKAGE_CONTENT_PATHS:
            path = getattr(__package.paths, key)
            content = getattr(__package.content, key)
            yield (path, content)

    def __build_files(__package: PYPIPackage):
        config_str = _init.init_pypipackage_config_str_method(__package)
        for (path, content) in __iter_package_path_content(__package):
            formatted_content = config_str(content)
            os.writes(path, content=formatted_content, is_abspath=True)

    def __report_files(__package: PYPIPackage):
        paths = []
        for (path, content) in __iter_package_path_content(__package):
            message = f"writing content to {path}:\n\n{content}\n\n"
            paths.append(path)
            print(message)
        paths = "\n".join(paths)

    def __build_package_content(__package: PYPIPackage):
        build_files = __package.config.build.build_files
        return (__build_files if build_files else __report_files)(__package)

    def __process_package_installation(__package: PYPIPackage):
        config = __package.config
        if config.build.autoinstall:
            content = __package.content
            private_install_locally_command = content.private_install_locally_command
            private_install_locally_command = f"cd {config.package.parentdir}/{config.package.name};{private_install_locally_command}"
            if private_install_locally_command:
                message = f"running {private_install_locally_command}"
                print(message)
                os.system(private_install_locally_command)

    def __mk_package_filetree(__package: PYPIPackage):
        subdir_structure = _init.init_pypipackage_config_str_method(__package)(
            _constants.SUBDIR_STRUCTURE
        )
        parentdir = __package.config.package.parentdir
        if parentdir:
            if __package.config.build.build_files:
                print(
                    "making filetree:", subdir_structure, "\n", "parentdir:", parentdir
                )
                os.mk_filetree(subdir_structure, parentdir=parentdir)
        else:
            print("no parentdir")

    if __package is not None:
        for build_method in (
            __mk_package_filetree,
            __build_package_content,
            __process_package_installation,
        ):
            build_method(__package)
