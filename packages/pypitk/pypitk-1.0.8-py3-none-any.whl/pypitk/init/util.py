def init_formatted_package_path(__package_name: str, path: str):
    name_error = f"/{__package_name}/{__package_name}/"
    result = path
    if name_error in path:

        while name_error in result:
            result = result.replace(name_error, f"/{__package_name}/")
        while result.endswith(f"/{__package_name}/{__package_name}"):
            result = result.removesuffix(f"/{__package_name}")
    return result


def format_template(__template: str, keymap: dict[str, str], delimiter: str = "*"):
    result = __template
    if delimiter in __template:
        for key, value in keymap.items():
            dkey = f"{delimiter}{key}{delimiter}"
            if dkey in result:
                result = result.replace(dkey, value)
    return result


def __iter_field_identifiers(__field_id: str, __parent_id: str, __delimiters):
    return iter(
        [f"*{__field_id}*"]
        + [f"*{__parent_id}{delim}{__field_id}*" for delim in __delimiters]
    )


def __subconfig_dicts(__config):
    return dict(
        package=__config.package.dict(),
        build=__config.build.dict(),
        pypi=__config.pypi.dict(),
    )


def __iter_configstr_pairs(__config, __delimiters):
    for subconfig_id, subconfig_dict in __subconfig_dicts(__config).items():
        for key, value in subconfig_dict.items():
            formatted_value = str(value) if isinstance(value, bool) else value
            for field_id in __iter_field_identifiers(key, subconfig_id, __delimiters):
                yield (field_id, formatted_value)


def __batchreplace(__str: str, __kviterator):
    result = str(__str)
    if isinstance(__kviterator, dict):
        __kviterator = iter(__kviterator.items())
    for (lhs, rhs) in __kviterator:
        result = result.replace(lhs, rhs)
    return result


def __init_config_str_method(__config, __delimiters):
    def config_str(__str: str):
        return (
            __batchreplace(__str, __iter_configstr_pairs(__config, __delimiters))
            if "*" in __str
            else str(__str)
        )

    return config_str


def init_configstr_method(__config, __delimiters):
    return __init_config_str_method(__config, __delimiters)
