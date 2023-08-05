import osiotk as _os
from .. import constants as _constants
from ..objects import PYPIPackage
from .. import init as _init


def __upgrade_version(__str: str):
    if "." in __str:
        try:
            components = [int(component) for component in __str.split(".", 2)]
            upgraded = False
            for (i, e) in enumerate(components):
                if e == 9:
                    if i > 0:
                        components[i] = 0
                        components[i - 1] += 1
                        upgraded = True
            if not upgraded:
                components[-1] += 1
                upgraded = True
            result = ".".join(str(component) for component in components)
            if result == __str:
                print("error: unable to upgrade package version")
                result = None
        except BaseException as error:
            print(error)
            result = None
    else:
        result = None
    return result


def update_pypipackage(__pypipackage: PYPIPackage = None):

    if __pypipackage is not None:
        version = __pypipackage.config.package.version
        new_version = __upgrade_version(__pypipackage.config.package.version)

        if new_version is not None:
            config_str = _init.init_pypipackage_config_str_method(__pypipackage)
            __pypipackage.config.package.version = new_version
            name = _init.init_formatted_package_name(__pypipackage.config.package.name)
            __pypipackage.config.package.name = name
            __pypipackage.config.package.parentdir = _init.init_formatted_package_path(
                name, __pypipackage.config.package.parentdir
            )

            for key in PYPIPackage.Content.__fields__.keys():
                value = getattr(__pypipackage.content, key)
                formatted_str = config_str(value)
                content = formatted_str.replace(str(version), str(new_version))
                assert version not in content, "version remains in content"
                setattr(__pypipackage.content, key, content)
                if key in _constants.FILENAMES_PACKAGE_CONTENT_PATHS:
                    path = _init.init_formatted_package_path(
                        name, getattr(__pypipackage.paths, key)
                    )
                    _os.writes(path, content=content, is_abspath=True)
            __pypipackage.save_to(__pypipackage.paths.pypitk_package, is_abspath=True)
            message = "updated package"
        else:
            message = "unable to update package: new_version is None"

    else:
        message = "unable to update package: package is None"
    print(message)
