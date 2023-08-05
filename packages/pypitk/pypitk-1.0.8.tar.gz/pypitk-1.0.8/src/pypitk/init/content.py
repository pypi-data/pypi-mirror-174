from typing import Callable
from .. import constants as _constants
from .. import objects as _objects
from . import util as _util
from ..pydantic_model import PydanticModel, Field


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


commandstr = lambda __name,__command:f"# {__name.title()}:\n#    {__command}"



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
        result.public_command = commandstr(result.description, result.public)
    if (not result.private_command) and (result.private):
        result.private_command = commandstr(result.description, result.private)
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

    readme = _util.format_template(_constants.TEMPLATE_README, public_config_values)
    private = config_str(
        _util.format_template(
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


def __get_content_dict_from_config(__config: _objects.PYPIPackage.Config, __delimiters):
    package_dict = __config.package.dict()
    config_str = _util.init_configstr_method(__config, __delimiters)
    commands_dict = __get_commands_dict(config_str=config_str)
    pypitk_config = __config.json(indent=4)
    return __get_content_dict(
        package_dict=package_dict,
        pypitk_config=pypitk_config,
        config_str=config_str,
        commands_dict=commands_dict,
    )


def __init_content_from_config(__config: _objects.PYPIPackage.Config, __delimiters):
    config_dict = __get_content_dict_from_config(__config, __delimiters)
    return _objects.PYPIPackage.Content(**config_dict)


def init_content_from_config(
    __config: _objects.PYPIPackage.Config, __delimiters=_constants.FIELD_DELIMITERS
):
    return __init_content_from_config(__config, __delimiters)
