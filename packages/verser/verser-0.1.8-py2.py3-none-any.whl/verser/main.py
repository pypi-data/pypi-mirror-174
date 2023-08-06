# import verser
from verser.verserLocal.components.increment_functions import increment_version_pypi, next_version_with_package_name, \
    next_version, next_version_pypi, next_version_local

from verser.verserLocal.components.increment_functions import *
from verser.verserLocal.components.project import Project
from verser.verserLocal.components.version_parts import *

assert callable(increment_version_pypi)
assert callable(next_version)

assert callable(next_version_pypi)
assert callable(next_version_with_package_name)
assert callable(Project)
assert callable(Project)

# r = increment_version_pypi("requests", part='minor')
# print(r)
#
# nv = increment_version_pypi(package_name="evdspy")
# print(nv)

# nv = next_version_with_package_name(package_name="rich")
# print(nv)

# from pathlib import Path
#
# project = Project('verser', version_file_path=Path('__version__.py'))
# nv = next_version(project, write=True)
# print(nv)
