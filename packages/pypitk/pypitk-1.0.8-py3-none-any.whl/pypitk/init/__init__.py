from typing import Callable, Iterable
from json import loads as __init_kwargs_from_jsonsrc
import osiotk as _os
from ..pydantic_model import PydanticModel, Field
from .. import objects
from .. import constants as _constants
from . import paths as _paths
from . import content as _contentinit
from . import util as _initutil


def __util_str_is_true(__str: str) -> bool:
    base = __str.lower().strip()
    return base in ("tr", "tru", "true") if base.startswith("t") else False


def __util_format_parentdir(__parentdir: str, name: str):
    result = __parentdir
    while result.endswith("/") and len(result) > 1:
        result = result[:-1]
    result += "/"
    if not result.endswith(name):
        result += name
    if result.startswith("~"):
        result = result[1:]
    if not result.startswith("/"):
        result = "/" + result
    return result


def __util_get_class_fields(__cls) -> list[str]:
    result = []
    try:
        for field_key in ("__dataclass_fields__", "__fields__"):
            result = getattr(__cls, field_key, None)
            if result is not None:
                result = list(result.keys() if isinstance(result, dict) else result)
                break
    except BaseException:
        result = None
    return result


def __init_formatted_package_name(__package_name: str):
    result = __package_name
    while "/" in result:
        name = result.split("/")[-1]
        if name:
            result = name
    return result


def __init_formatted_package_path(__package_name: str, path: str):
    name_error = f"/{__package_name}/{__package_name}/"
    result = path
    if name_error in path:

        while name_error in result:
            result = result.replace(name_error, f"/{__package_name}/")
        while result.endswith(f"/{__package_name}/{__package_name}"):
            result = result.removesuffix(f"/{__package_name}")
    return result


def __iter_field_identifier_pairs(__cls, delimiters: Iterable):
    prefix = str(__cls.__prefix__)
    for field_name in __util_get_class_fields(__cls):
        yield (prefix, field_name, field_name)
        for delimiter in delimiters:
            yield (prefix, field_name, f"{prefix}{delimiter}{field_name}")


def __match_field_key(__key: str, __subconfig, delimiters: Iterable = None):
    result = None
    for (parent, name, comparator_name) in __iter_field_identifier_pairs(
        __subconfig, delimiters=delimiters
    ):
        if __key == comparator_name:
            result = dict(parent=parent, key=name)
            break
    return result


def __postinit_varline(__varline: dict, __subconfigs, delimiters: Iterable = None):
    parent = __varline["parent"]
    if not parent:
        key = __varline["key"]
        for subconfig in __subconfigs:
            match = __match_field_key(key, subconfig, delimiters=delimiters)
            if match is not None:
                __varline.update(match)
                break
    return __varline


class _VarLine(PydanticModel):
    key: str = Field("")
    parent: str = Field("")
    value: str = Field("")
    is_varline: bool = Field(False)


def __varline_key_parent(key: str):
    parts = None
    for delim in ("_", "."):
        if delim in key:
            parts == key.split(delim, 1)
            break
    if parts is None:
        parts = [key, ""]
    return parts[0], parts[1]


def __init_varline(
    line: str, asdict: bool = False, postinit_varline: Callable[[dict], dict] = None
):
    if "=" in line:
        kv = line.split("=", 1)
        key = kv[0].strip()
        value = kv[1].lstrip()
        key, parent = __varline_key_parent(key=key)
        result = _VarLine(key=key, value=value, parent=parent, is_varline=True)
    else:
        result = _VarLine()
    if asdict:
        result = result.dict()
    if postinit_varline is not None:
        result = postinit_varline(result)
    return result


def __build_varline_postinit(__subconfigs, delimiters: Iterable = None):
    if delimiters is None:
        delimiters = _constants.FIELD_DELIMITERS

    def postinit_varline(__varline: dict):
        return __postinit_varline(__varline, __subconfigs, delimiters=delimiters)

    return postinit_varline


def __varlines_from_src(src: str, postinit_varline):
    assert isinstance(src, str), __name__ + " src is not string"
    result = []
    for line in src.splitlines(keepends=False):
        _varline = __init_varline(line, asdict=True, postinit_varline=postinit_varline)
        if _varline is not None:
            if _varline.get("is_varline", False):
                result.append(_varline)
    return result


def __init_config_kwargs_from_varlines(__varlines: list[dict]):
    results = {}
    for varline in (varline for varline in __varlines if isinstance(varline, dict)):
        parent = varline.get("parent", None)
        if parent:
            if not parent in results:
                results[parent] = {}
            key = varline.get("key", None)
            if key:
                value = varline.get("value", None)
                results[parent][key] = value
    return results


def __init_config_kwargs_from_rawsrc(__src: str):

    subconfigs = objects.PYPIPackage.Config.__subconfigs__
    postinit_varline = __build_varline_postinit(subconfigs)
    varlines = __varlines_from_src(src=__src, postinit_varline=postinit_varline)
    kwargs = __init_config_kwargs_from_varlines(varlines)
    return kwargs


def __init_config_kwargs_from_src(__src: str):
    try:
        result = __init_kwargs_from_jsonsrc(__src)
    except BaseException:
        result = None
    if not result:
        try:
            result = __init_config_kwargs_from_rawsrc(__src)
        except BaseException:
            result = None
    return result


def __init_config_kwargs_from_json_path(__path: str, is_abspath: bool):
    return _os.readjson(__path, is_abspath)


def __init_config_kwargs_from_rawpath(__path: str, is_abspath: bool):
    src = _os.reads(__path, is_abspath=is_abspath)
    return __init_config_kwargs_from_rawsrc(src)


def __init_config_kwargs_from_path(__path: str, is_abspath: bool):
    return (
        __init_config_kwargs_from_json_path
        if __path.endswith(".json")
        else __init_config_kwargs_from_rawpath
    )(__path, is_abspath)


def __init_config_kwargs(
    __src: str = None, __path: str = None, is_abspath: bool = False
):
    if __src:
        result = __init_config_kwargs_from_src(__src)
    else:
        result = __init_config_kwargs_from_path(
            __path,
            is_abspath=is_abspath,
        )
    assert result is not None, __name__ + ".error: result is none"
    return result


def __init_pypipackage_build_subconfig(kwargs: dict = None):
    if kwargs is not None:
        kwargs_ = {key: "" if value is None else value for key, value in kwargs.items()}
        result = objects.PYPIPackage.Config.Build(**kwargs_)
    else:
        result = objects.PYPIPackage.Config.Build()
    if isinstance(result.autoinstall, str):
        result.autoinstall = __util_str_is_true(result.autoinstall)
    if isinstance(result.build_files, str):
        result.build_files = __util_str_is_true(result.build_files)
    return result


def __init_pypipackage_package_subconfig(kwargs: dict = None):
    _kwargs = {} if kwargs is None else kwargs
    result = objects.PYPIPackage.Config.Package(**_kwargs)
    result.parentdir = __util_format_parentdir(result.parentdir, result.name)
    return result


def __init_pypipackage_pypi_subconfig(kwargs: dict = None):
    kwargs_ = {} if kwargs is None else kwargs
    result = objects.PYPIPackage.Config.PYPI(**kwargs_)
    return result


def __pypipackage_config_subconfig_init(__subconfig_id: str):
    return {
        "pypi": __init_pypipackage_pypi_subconfig,
        "build": __init_pypipackage_build_subconfig,
        "package": __init_pypipackage_package_subconfig,
    }[__subconfig_id]


def __init_pypipackage_config_from_kwargs(kwargs: dict = None):
    kwargs_ = {} if not kwargs else kwargs
    results = {}
    for subconfig_id in (
        subconfig.__prefix__ for subconfig in objects.PYPIPackage.Config.__subconfigs__
    ):
        subconfig_init = __pypipackage_config_subconfig_init(subconfig_id)
        subconfig_kwargs = kwargs_[subconfig_id]
        subconfig = subconfig_init(subconfig_kwargs)
        results[subconfig_id] = subconfig
    config = objects.PYPIPackage.Config(**results)
    config.package.parentdir = __init_formatted_package_path(
        config.package.name, config.package.parentdir
    )
    return config


def __init_pypipackage_config(src_path: str = None, pypitk_config: str = None):
    kwargs = __init_config_kwargs(pypitk_config, src_path, is_abspath=True)
    config = __init_pypipackage_config_from_kwargs(kwargs=kwargs)
    return config


def __postinit_pypipackage(__pypipackage: objects.PYPIPackage):
    def __postinit_pypackage_config(__pypipackage: objects.PYPIPackage):
        __pypipackage.config.package.name = __init_formatted_package_name(
            __pypipackage.config.package.name
        )
        __pypipackage.config.package.parentdir = __init_formatted_package_path(
            __pypipackage.config.package.name, __pypipackage.config.package.parentdir
        )
        return __pypipackage

    def __postinit_pypackage_filenames(__pypipackage: objects.PYPIPackage):
        for content_path_key in _constants.FILENAMES_PACKAGE_CONTENT_PATHS:
            path = getattr(__pypipackage.paths, content_path_key)
            formatted_path = __init_formatted_package_path(
                __pypipackage.config.package.name, path
            )
            setattr(__pypipackage.paths, content_path_key, formatted_path)
        return __pypipackage

    __pypipackage = __postinit_pypackage_config(__pypipackage)
    __pypipackage = __postinit_pypackage_filenames(__pypipackage)
    __pypipackage.content.pypitk_package = __pypipackage.json(indent=4)
    return __pypipackage


def __init_pypipackage_from_config(__config):
    paths = _paths.init_pypipackage_paths(config=__config)
    content = _contentinit.init_content_from_config(__config)
    result = objects.PYPIPackage(config=__config, paths=paths, content=content)
    return __postinit_pypipackage(result)


def __init_pypipackage_from_config_path(__config_path: str):
    config = __init_pypipackage_config(src_path=__config_path)
    return __init_pypipackage_from_config(config)


def __init_pypipackage_from_paths(
    package_path: str = None, config_path: str = None, parentdir: str = None
):
    if package_path:
        result = objects.PYPIPackage.init_from(package_path)
    elif config_path:
        result = __init_pypipackage_from_config_path(config_path)
    elif parentdir:
        result = __init_pypipackage_from_parentdir(parentdir)
    else:
        print("unable to init pypi package from paths")
        result = None
    return result


def __init_pypipackage_from_systemargs(__systemargs: dict[str, dict] = None):
    if "config_path" in __systemargs:
        path = __systemargs["config_path"]
        if isinstance(path, dict):
            path = path["value"]
        result = __init_pypipackage_from_paths(config_path=path)
        if result is not None:
            if _os.file_exists(result.paths.pypitk_package, is_abspath=True):
                try:
                    result = objects.PYPIPackage.parse_file(
                        path=result.paths.pypitk_package
                    )
                except BaseException as error:
                    print("result parser failed", error)
    elif "package_path" in __systemargs:
        path = __systemargs["package_path"]
        if isinstance(path, dict):
            path = path["value"]
        result = __init_pypipackage_from_paths(package_path=path)
    else:
        result = None
    return result


def __init_pypipackage_from_parentdir(__parentdir: str) -> objects.PYPIPackage:
    name = _os.basename(__parentdir)
    paths = _paths.init_pypipackage_paths(parentdir=__parentdir, package_name=name)
    if _os.file_exists(paths.pypitk_package):
        pypipackage = objects.PYPIPackage.parse_file(paths.pypitk_package)
    elif _os.file_exists(paths.pypitk_config):
        pypipackage = __init_pypipackage(config_path=paths.pypitk_config)
    else:
        pypipackage = None
    return pypipackage


def __init_pypipackage(
    package_path: str = None,
    config_path: str = None,
    parentdir: str = None,
    system_args: dict[str, dict] = None,
):

    if package_path or config_path or parentdir:
        result = __init_pypipackage_from_paths(
            package_path=package_path, config_path=config_path, parentdir=parentdir
        )
    elif system_args:
        result = __init_pypipackage_from_systemargs(system_args)
    else:
        result = None
    return result


def __get_pypiprocess_task(__system_args: dict[str, dict], default: str = "create"):

    task = next(
        (key for key in __system_args.keys() if key in _constants.CLI_COMMANDS),
        default,
    )
    if task and task in __system_args:
        del __system_args[task]
    return task


def __get_pypiprocess_kwargs(__system_args: dict[str, dict], __field_ids):
    kwargs = dict(task=__get_pypiprocess_task(__system_args))
    for field_id in __field_ids:
        if not field_id in kwargs and field_id in __system_args:
            kwargs[field_id] = __system_args[field_id]["value"]
    return kwargs


def __init_pypiprocess(__system_args: dict[str, dict]):
    kwargs = __get_pypiprocess_kwargs(
        __system_args, objects.PYPIProcess.__fields__.keys()
    )
    return objects.PYPIProcess(**kwargs)


def init_pypipackage(
    package_path: str = None,
    config_path: str = None,
    system_args: dict[str, dict] = None,
):
    return __init_pypipackage(
        package_path=package_path, config_path=config_path, system_args=system_args
    )


def init_pypipackage_config(src_path: str = None, pypitk_config: str = None):
    return __init_pypipackage_config(src_path=src_path, pypitk_config=pypitk_config)


def init_pypipackage_config_str_method(__package: objects.PYPIPackage):
    return _initutil.init_configstr_method(
        __package.config, _constants.FIELD_DELIMITERS
    )


def init_pypiprocess(__system_args: dict[str, dict]):
    return __init_pypiprocess(__system_args)


def init_formatted_package_path(__package_name: str, path: str):
    return __init_formatted_package_path(__package_name, path=path)


def init_formatted_package_name(__package_name: str):
    return __init_formatted_package_name(__package_name)
