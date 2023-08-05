from typing import Callable, Iterable
from json import loads as __init_kwargs_from_jsonsrc
import osiotk as _os
from . import objects
from .pydantic_model import PydanticModel, Field
from . import constants as _constants


def __util_format_template(
    __template: str, keymap: dict[str, str], delimiter: str = "*"
):
    result = __template
    if delimiter in __template:
        for key, value in keymap.items():
            dkey = f"{delimiter}{key}{delimiter}"
            if dkey in result:
                result = result.replace(dkey, value)
    return result


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


def __util_form_command(__name: str, command: str):
    return f"# {__name.title()}:\n#    {command}"


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


# init paths
def __init_pypipackage_paths_base(parentdir: str, package_name: str):
    parentdir = __init_formatted_package_path(package_name, path=parentdir)
    joinpath = lambda __name: __init_formatted_package_path(
        package_name, _os.join_paths(parentdir, __name)
    )

    constant_kwargs = {
        path_id: f"FILENAME_{path_id.upper()}"
        for path_id in objects.PYPIPackage.Data.__fields__.keys()
    }
    constant_data = {
        path_id: getattr(_constants, constant_id)
        for path_id, constant_id in constant_kwargs.items()
    }
    kwargs = {
        path_id: joinpath(path_data) for path_id, path_data in constant_data.items()
    }
    result = objects.PYPIPackage.Paths(**kwargs)
    result.pypi_path = f"https://pypi.org/project/{package_name}/"
    return result


def __init_pypipackage_paths_from_package(
    __package: objects.PYPIPackage.Config.Package,
):
    parentdir = __package.parentdir
    name = __package.name
    return __init_pypipackage_paths_base(parentdir=parentdir, package_name=name)


def __init_pypipackage_paths_from_config(__config: objects.PYPIPackage.Config):
    package = __config.package
    return __init_pypipackage_paths_from_package(package)


def __init_pypipackage_paths(
    parentdir: str = None,
    package_name: str = None,
    config: objects.PYPIPackage.Config = None,
):
    config_is_not_none = config is not None
    can_initialize_from_package_params = (
        parentdir is not None and package_name is not None
    )

    assert (
        config_is_not_none or can_initialize_from_package_params
    ), "unable to initialize pypipackage paths from given parameters"

    return (
        __init_pypipackage_paths_base(parentdir, package_name)
        if can_initialize_from_package_params
        else __init_pypipackage_paths_from_config(config)
    )


class _Command(PydanticModel):
    id: str = Field("")
    description: str = Field("")
    public: str = Field("")
    private: str = Field("")
    public_command: str = Field("")
    private_command: str = Field("")


class _Commands(PydanticModel):

    install_poetry: _Command = Field()
    build_package: _Command = Field()
    publish_package: _Command = Field()
    install_package: _Command = Field()
    build_publish: _Command = Field()
    build_publish_install: _Command = Field()
    test: _Command = Field()

    def __iter__(self):
        return (getattr(self, key) for key in self.__fields__.keys())

    @property
    def commands(self) -> list[_Command]:
        return list(self)

    @property
    def public_commands(self) -> list[str]:
        return [
            command.public_command
            for command in self.commands
            if command.public_command
        ]

    @property
    def private_commands(self) -> list[str]:
        return [
            command.private_command
            for command in self.commands
            if command.private_command
        ]


def __init_command(
    command: dict, config_str: Callable[[str], str], asdict: bool = False
):
    if not "private" in command:
        command["private"] = command["public"]
    for key in command.keys():
        command[key] = config_str(command[key])
    result = _Command(**command)
    result.private = result.private if result.private else result.public
    if (not result.public_command) and (result.public):
        result.public_command = __util_form_command(result.description, result.public)
    if (not result.private_command) and (result.private):
        result.private_command = __util_form_command(result.description, result.private)
    if asdict:
        result = result.dict()
    return result


def __init_commands(config_str: Callable[[str], str]):
    result = {}
    for command in _constants.COMMAND_TEMPLATES.copy():
        command = __init_command(command=command, config_str=config_str)
        result[command.id] = command
    result = _Commands(**result)
    return result


def __get_commands_dict(config_str: Callable[[str], str]):
    commands = __init_commands(config_str=config_str)
    __cmdstr = lambda __cmds: "\n\n".join(__cmds)
    public_commands = __cmdstr(commands.public_commands)
    private_commands = __cmdstr(commands.private_commands)
    private_build_publish_install = commands.build_publish_install.private
    return dict(
        public_commands=public_commands,
        private_commands=private_commands,
        private_build_publish_install=private_build_publish_install,
    )


def __build_config_values(__commands_dict: dict, __package_dict):

    config_values = {}
    name = str(__package_dict["name"]).title()
    description = str(__package_dict["description"])
    base_values = dict(name=name, description=description)
    for privacy_id in ("public", "private"):
        key = f"{privacy_id}_commands"
        values = base_values.copy()
        values["commands"] = __commands_dict[key]
        config_values[privacy_id] = values
    return config_values


def __get_content_dict(
    package_dict: dict,
    pypitk_config: str,
    config_str: Callable[[str], str],
    commands_dict: dict[str, str],
):

    pyproject_toml = config_str(_constants.TEMPLATE_PYPROJECT_TOML)
    config_values = __build_config_values(commands_dict, package_dict)
    public_config_values = config_values["public"]
    private_config_values = config_values["private"]

    readme = __util_format_template(_constants.TEMPLATE_README, public_config_values)
    private = config_str(
        __util_format_template(
            _constants.TEMPLATE_PRIVATE_COMMANDS, private_config_values
        )
    )

    private_build_publish_install = commands_dict["private_build_publish_install"]

    return dict(
        readme=readme,
        pyproject_toml=pyproject_toml,
        private=private,
        private_install_locally_command=private_build_publish_install,
        pypitk_config=pypitk_config,
    )


def __get_content_dict_from_config(__config: objects.PYPIPackage.Config):
    package_dict = __config.package.dict()
    config_str = __init_config_str_method(__config)
    commands_dict = __get_commands_dict(config_str=config_str)
    pypitk_config = __config.json(indent=4)
    return __get_content_dict(
        package_dict=package_dict,
        pypitk_config=pypitk_config,
        config_str=config_str,
        commands_dict=commands_dict,
    )


def __init_content_from_config(__config: objects.PYPIPackage.Config):
    config_dict = __get_content_dict_from_config(__config)
    return objects.PYPIPackage.Content(**config_dict)


def __iter_field_identifiers(__field_id: str, parent_id: str):
    return iter(
        [f"*{__field_id}*"]
        + [f"*{parent_id}{delim}{__field_id}*" for delim in _constants.FIELD_DELIMITERS]
    )


def __subconfig_dicts(__config: objects.PYPIPackage.Config):
    return dict(
        package=__config.package.dict(),
        build=__config.build.dict(),
        pypi=__config.pypi.dict(),
    )


def __config_str_method_base(__config: objects.PYPIPackage.Config, __str: str):
    result = str(__str)
    if "*" in result:
        for subconfig_id, subconfig_dict in __subconfig_dicts(__config).items():
            for key, value in subconfig_dict.items():
                formatted_value = str(value) if isinstance(value, bool) else value
                for field_id in __iter_field_identifiers(key, parent_id=subconfig_id):
                    result = result.replace(field_id, formatted_value)
    return result


def __init_config_str_method(__config: objects.PYPIPackage.Config):
    def config_str(__str: str):
        return __config_str_method_base(__config, __str)

    return config_str


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


def init_pypipackage_config_str_method(__config: objects.PYPIPackage.Config):
    return __init_config_str_method(__config)


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
    paths = __init_pypipackage_paths_from_config(__config)
    content = __init_content_from_config(__config)
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
    paths = __init_pypipackage_paths(parentdir=__parentdir, package_name=name)
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
    return __init_config_str_method(__package.config)


def init_pypiprocess(__system_args: dict[str, dict]):
    return __init_pypiprocess(__system_args)


def init_pypipackage_paths(
    parentdir: str = None,
    package_name: str = None,
    config: objects.PYPIPackage.Config = None,
):
    return __init_pypipackage_paths(
        parentdir=parentdir, package_name=package_name, config=config
    )


def init_formatted_package_path(__package_name: str, path: str):
    return __init_formatted_package_path(__package_name, path=path)


def init_formatted_package_name(__package_name: str):
    return __init_formatted_package_name(__package_name)
