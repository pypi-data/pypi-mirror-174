from .build_pypipackage import build_package as _build_pypipackage
from .update_pypipackage import update_pypipackage as _update_pypipackage
from .. import objects


def build(__pypipackage: objects.PYPIPackage):
    return _build_pypipackage(__pypipackage)


def update(__pypipackage: objects.PYPIPackage):
    return _update_pypipackage(__pypipackage)
