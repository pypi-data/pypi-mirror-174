from enum import Enum
import typing as t
from rich import inspect
from pathlib import Path

from verser.verserLocal.components.version_functions import check_and_write
from verser.verserLocal.components.version_parts import VersionParts
from verser.verserLocal.api.pypi_latest import get_latest_version
from verser.verserLocal.enums.parts_enum import get_enum_with_value, VersionPartEnum, major, minor, patch, pre, build
from verser.verserLocal.components.project import Project

import typing as t


def build_version_from_instance_major(prev_instance):
    v = VersionParts(str(prev_instance.major_num), "0", "0", "", "")
    return v


def build_version_from_instance_minor(prev_instance):
    v = VersionParts(str(prev_instance.major_num), str(prev_instance.minor_num), '0', "", "")
    return v


def build_version_from_instance_patch(prev_instance):
    v = VersionParts(str(prev_instance.major_num), str(prev_instance.minor_num), str(prev_instance.patch_num), "", "")
    return v


def build_version_from_instance_pre(prev_instance):
    v = VersionParts(str(prev_instance.major_num), str(prev_instance.minor_num), str(prev_instance.patch_num),
                     str(prev_instance.prerelease_num), "")
    return v


def build_version_from_instance_build(prev_instance):
    v = VersionParts(str(prev_instance.major_num), str(prev_instance.minor_num), str(prev_instance.patch_num),
                     str(prev_instance.prerelease_num), str(prev_instance.buildmetadata_num))
    return v


#

def increment_version(
        prev_instance: VersionParts,
        part: t.Union[str, Enum] = "patch",
        increment_choice: bool = True,

) -> VersionParts:
    if not increment_choice:
        print("not incrementing due to parameter increment.")
        return build_version_from_instance_major(prev_instance)

    part_enum = get_enum_with_value(part, VersionPartEnum, patch)
    assert part_enum is not None
    next_instance = prev_instance

    if part_enum == major:
        next_instance = prev_instance
        next_instance.major_num = prev_instance.major_num + 1
        next_instance = build_version_from_instance_major(next_instance)
    if part_enum == minor:
        next_instance = prev_instance
        next_instance.minor_num = prev_instance.minor_num + 1
        next_instance = build_version_from_instance_minor(next_instance)
    if part_enum == patch:
        next_instance = prev_instance
        next_instance.patch_num = prev_instance.patch_num + 1
        next_instance = build_version_from_instance_patch(next_instance)

    if part_enum == pre:
        next_instance = prev_instance
        prev_instance.prerelease_num = prev_instance.prerelease_num + 1
        next_instance = build_version_from_instance_pre(next_instance)
    if part_enum == build:
        next_instance = prev_instance
        next_instance.buildmetadata_num = prev_instance.buildmetadata_num + 1
        next_instance = build_version_from_instance_build(next_instance)

    return next_instance


def onload_increment():
    # v = increment_version_string("1.0.5-rc.1+build.12")
    v = increment_version_string("1.0.5")
    # inspect(v)
    if v:
        print(v.info)
    else:
        print("did not read v ")


def increment_version_string(version_str: str, increment_choice=True, part="patch"):
    from verser.verserLocal.components.version_functions import create_version_instance
    if isinstance(version_str, VersionParts):
        version_str = str(version_str)
    v = create_version_instance(version_str)

    v2 = increment_version(v, increment_choice=increment_choice, part=part)

    return v2


# onload_increment()
def increment_version_pypi(package_name="verser", increment_choice=True, part="patch", write=True):
    """ checks the latest version of your package from PYPI and increments part"""
    from verser.verserLocal.components.version_functions import create_version_instance
    latest_version = get_latest_version(package_name)
    if not latest_version:
        return False
    version_instance = create_version_instance(latest_version.version_text)
    next_version_instance = increment_version_string(
        version_str=str(version_instance),
        increment_choice=increment_choice,
        part=part,

    )
    if_write_then_write(write, package_name, next_version_instance)
    return next_version_instance


def next_version(
        project: Project = Project(),
        part='patch',  # build / pre / patch / minor / major
        pypi=True,  # to increment checking the latest version on PYPI // default : local version file
        write=True
):
    from verser.verserLocal.components.version_functions import create_version_instance, get_current_version_instance

    if pypi:
        if not project:
            print(
                "When PYPI parameter is True project should be provided as project= Project('xyz' , '')")
            return False
        package_name = project.package_name
        if isinstance(package_name, Project):
            package_name = Project.package_name

        latest_version = get_latest_version(package_name)
        if not latest_version:
            return next_version(project=project, part=part, pypi=False, write=write)
        latest_version_text = create_version_instance(latest_version.version_text)
    else:
        latest_version_text = get_current_version_instance(
            project)
    next_version_instance: VersionParts = increment_version_string(
        version_str=latest_version_text,
        increment_choice=True,
        part=part
    )
    if_write_then_write(write, project, next_version_instance)
    return next_version_instance


def if_write_then_write(write: bool, project: t.Union[Project, str], next_version_instance: t.Union[VersionParts, str]):
    if write:
        next_version_text = str(next_version_instance)
        check_and_write(project, next_version_text)


def next_version_with_package_name(
        package_name: t.Union[str, Project] = None,
        part='patch',  # build / pre / patch / minor / major
        pypi=False,  # to increment checking latest version on PYPI default : local version file
        write=True
):
    from verser.verserLocal.components.version_functions import create_version_instance, get_current_version_instance
    if isinstance(package_name, Project):
        project = package_name
    else:
        project = Project(
            package_name=package_name,
            version_file_path=Path('__version__.py')
        )

    if pypi:

        # if isinstance(package_name, Project):
        #     package_name = Project.package_name

        latest_version = get_latest_version(Project.package_name)
        latest_version_text = create_version_instance(latest_version.version_text)
    else:

        latest_version_text = get_current_version_instance(
            project)

    next_version_instance = increment_version_string(
        version_str=latest_version_text,
        increment_choice=True,
        part=part
    )
    if_write_then_write(write, project, next_version_instance)
    return next_version_instance


def next_version_pypi(package_name: str, increment_choice: bool = True, part: str = "patch", write=True):
    next_version_instance = increment_version_pypi(
        package_name=package_name,
        increment_choice=increment_choice,
        part=part,
        write=write,
    )
    if_write_then_write(write, package_name, next_version_instance)
    return next_version_instance


def get_project_from_package_name(package_name: t.Union[str, Project]) -> Project:
    if isinstance(package_name, str):
        package_name = Project(
            package_name=package_name,
            version_file_path=Path('__version__.py'))
    return package_name


def next_version_local(package_name: Project, increment_choice: bool = True, part: str = "patch", write=True):
    from verser.verserLocal.components.version_functions import create_version_instance, get_current_version_instance
    project = get_project_from_package_name(package_name)
    latest_version_text = get_current_version_instance(
        project
    )
    next_version_instance = increment_version_string(
        version_str=latest_version_text,
        increment_choice=increment_choice,
        part=part,

    )
    if_write_then_write(write, project, next_version_instance)
    return next_version_instance


__all__ = [
    'build_version_from_instance_major',
    'build_version_from_instance_minor',
    'increment_version',
    'onload_increment',
    'increment_version_string',
    'increment_version_pypi',

]
