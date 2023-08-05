from .pydantic_model import PydanticModel, Field


class PYPIPackageData(PydanticModel):

    readme: str = Field("")
    pyproject_toml: str = Field("")
    private: str = Field("")
    pypitk_package: str = Field("")


class PYPIPackage(PydanticModel):

    Data = PYPIPackageData

    class Config(PydanticModel):
        class Build(PydanticModel):

            __prefix__ = "build"

            autoinstall: bool = Field(False)
            subdir_structure: str = Field("")
            build_files: bool = Field(True)

        class Package(PydanticModel):

            __prefix__ = "package"

            name: str = Field("")
            parentdir: str = Field("")
            version: str = Field("")
            description: str = Field("")
            python_version: str = Field("")
            license: str = Field("")

        class PYPI(PydanticModel):

            __prefix__ = "pypi"

            username: str = Field("")
            password: str = Field("")
            email: str = Field("")

        package: Package = Field()
        pypi: PYPI = Field()
        build: Build = Field()

        __subconfigs__ = (Package, PYPI, Build)

    class Content(Data):

        private_install_locally_command: str = Field("")

    class Paths(Data):
        pypi_path: str = Field("")
        pass

    config: Config = Field()
    content: Content = Field()
    paths: Paths = Field()


class PYPIProcess(PydanticModel):

    config_path: str = Field("")
    task: str = Field("")
    open_in_finder: bool = Field(False)
    open_in_vscode: bool = Field(False)
    open_in_pypi: bool = Field(False)


class PYPIRuntime(PydanticModel):

    package: PYPIPackage = Field()
    process: PYPIProcess = Field()
    system_args: dict[str, dict] = Field()
