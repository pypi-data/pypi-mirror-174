import sysargstk as _sysargs
import osiotk as _os
from . import objects
from . import tasks
from . import init as _init


def __execute_runtime(__runtime: objects.PYPIRuntime):
    __task = __runtime.process.task
    if __task == "create":
        tasks.build(__runtime.package)
    elif __task == "update":
        tasks.update(__runtime.package)
    elif __task == "help":
        print("task=help")


def __postprocess_runtime(__runtime: objects.PYPIRuntime):
    parentdir = __runtime.package.config.package.parentdir
    commands = []
    if __runtime.process.open_in_finder:
        commands.append(f"open {parentdir}")
    if __runtime.process.open_in_vscode:
        commands.append(f"code {parentdir}")
    for command in commands:
        _os.system(command)


def __ensure_system_args(__system_args: dict[str, dict] = None):
    if __system_args is None:
        __system_args = _sysargs.dict()
    return __system_args


def __init_runtime(__system_args: dict[str, dict] = None):

    system_args = __ensure_system_args(__system_args)
    process = _init.init_pypiprocess(system_args)
    package = _init.init_pypipackage(system_args=system_args)
    return objects.PYPIRuntime(
        package=package, process=process, system_args=system_args
    )


def init_runtime(__system_args: dict[str, dict] = None):
    return __init_runtime(__system_args)


def execute(__runtime: objects.PYPIRuntime):
    __execute_runtime(__runtime)


def postprocess(__runtime: objects.PYPIRuntime):
    return __postprocess_runtime(__runtime)


def run(__system_args: dict[str, dict] = None):
    pypiruntime = __init_runtime(__system_args)
    __execute_runtime(pypiruntime)
    postprocess(pypiruntime)
