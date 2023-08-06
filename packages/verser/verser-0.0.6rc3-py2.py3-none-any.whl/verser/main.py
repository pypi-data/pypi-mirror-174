# import verser
from verser.verserLocal.components.increment_functions import increment_version_pypi, next_version_with_package_name, \
    next_version

from verser.verserLocal.components.increment_functions import *
from verser.verserLocal.components.project import Project
from verser.verserLocal.components.version_parts import *

assert callable(increment_version_pypi)

#
# r = increment_version_pypi("rich", part='minor')
# print(r)
#
# nv = increment_version_pypi(package_name="evdspy")
# print(nv)
#
# nv = next_version_with_package_name(package_name="rich")
# print(nv)
#
# from pathlib import Path
#
# project = Project('verser', version_file_path=Path('verser/__version__.py'))
# nv = next_version(project, write=True)
# print(nv)
