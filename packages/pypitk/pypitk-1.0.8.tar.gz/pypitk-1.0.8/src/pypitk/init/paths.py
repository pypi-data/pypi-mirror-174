import osiotk as _os
from .. import constants as _constants
from .. import objects as _objects
from .util import init_formatted_package_path as __init_formatted_package_path


def __init_pypipackage_paths_base(__parentdir: str, __package_name: str):
    __parentdir = __init_formatted_package_path(__package_name, path=__parentdir)
    joinpath = lambda __name: __init_formatted_package_path(
        __package_name, _os.join_paths(__parentdir, __name)
    )

    constant_kwargs = {
        path_id: f"FILENAME_{path_id.upper()}"
        for path_id in _objects.PYPIPackage.Data.__fields__.keys()
    }
    constant_data = {
        path_id: getattr(_constants, constant_id)
        for path_id, constant_id in constant_kwargs.items()
    }
    kwargs = {
        path_id: joinpath(path_data) for path_id, path_data in constant_data.items()
    }
    result = _objects.PYPIPackage.Paths(**kwargs)
    result.pypi_path = f"https://pypi.org/project/{__package_name}/"
    return result


def __init_pypipackage_paths_from_package(
    __package: _objects.PYPIPackage.Config.Package,
):
    parentdir = __package.parentdir
    name = __package.name
    return __init_pypipackage_paths_base(parentdir, name)


def __init_pypipackage_paths_from_config(__config: _objects.PYPIPackage.Config):
    package = __config.package
    return __init_pypipackage_paths_from_package(package)


def __init_pypipackage_paths(
    __parentdir: str = None,
    __package_name: str = None,
    __config: _objects.PYPIPackage.Config = None,
):
    config_is_not_none = __config is not None
    can_initialize_from_package_params = (
        __parentdir is not None and __package_name is not None
    )

    assert (
        config_is_not_none or can_initialize_from_package_params
    ), "unable to initialize pypipackage paths from given parameters"

    return (
        __init_pypipackage_paths_base(__parentdir, __package_name)
        if can_initialize_from_package_params
        else __init_pypipackage_paths_from_config(__config)
    )


def init_pypipackage_paths(
    parentdir: str = None,
    package_name: str = None,
    config: _objects.PYPIPackage.Config = None,
):
    return __init_pypipackage_paths(parentdir, package_name, config)
