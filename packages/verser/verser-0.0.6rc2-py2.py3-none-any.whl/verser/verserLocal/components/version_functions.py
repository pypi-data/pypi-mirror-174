from verser.verserLocal.components.project import Project
from verser.verserLocal.components.version_parts import VersionParts


# ------------------------------------------- (fnc) create_version_instance

def create_version_instance(version_str: str, project: Project = Project(), repeated=False) -> VersionParts:
    """creates versionParts instance from string  """

    if not valid_check(version_str):

        if not repeated:
            return create_version_instance(".".join(str(version_str).split(".")), project, repeated=True)

        print_with_failure_style(
            f"version : {version_str} does not fit to PEP. Continues with default start.{DEFAULT_START_VERSION}")
        version_str = DEFAULT_START_VERSION
    version_str = version_str.lower().replace("#", "").strip().replace("'", "")
    instance = VersionParts(*get_parts_from_version_string(version_str), original=version_str)
    return instance


import random

from verser.verserLocal.api.pypi_latest import get_latest_version
from verser.verserLocal.common.colors import *

from dataclasses import dataclass
from pathlib import Path
from dataclasses import dataclass
from verser.verserLocal.common.files import Read, Write
import typing as t
import random
import re

from verser.verserLocal.components.defaults import DEFAULT_START_VERSION
# from verser.verserLocal.components.increment_functions import increment_version
from verser.verserLocal.format.format_check import get_parts_from_version_string, valid_check
from verser.verserLocal.components.project import Project
from verser.verserLocal.components.version_parts import VersionParts

# # ------------------------------------------- (fnc) create_version_instance
# # from verser.verserLocal.components.create_version_functions import create_version_instance
# def create_version_instance(version_str: str, project: Project = Project()) -> VersionParts:
#     """creates versionParts instance from string  """
#     if not valid_check(version_str):
#         print_with_failure_style(
#             f"version : {version_str} does not fit to PEP. Continues with default start.{DEFAULT_START_VERSION}")
#         version_str = DEFAULT_START_VERSION
#     version_str = version_str.lower().replace("#", "").strip().replace("'", "")
#     instance = VersionParts(*get_parts_from_version_string(version_str), original=version_str)
#     return instance


from verser.verserLocal.components.display_version import display_version
# from verser.verserLocal.components.increment_functions import increment_version
from verser.verserLocal.components.mock_versions import mock_read
from verser.verserLocal.components.project import Project
from verser.verserLocal.components.version_parts import VersionParts


# from verser.verserLocal.format.format_check import get_parts_from_version_string, get_some_example_version_tuples, valid_check, \
#     get_some_example_version_string
#
# from verser.verserLocal.enums.parts_enum import get_enum_with_value, VersionPartEnum, major, minor, patch
#
# from verser.verserLocal.components.defaults import DEFAULT_START_VERSION
#
# from enum import Enum


class VersionNotFound(BaseException):
    """Version file not found """

    def __int__(self, *args):
        self.msg = f"Could find a proper version file, path may be given incorrectly path:  {', '.join(args)}"
        self.args = args

    def __str__(self):
        return self.msg


def get_previous(project: Project) -> str:
    """get_previous Gets current version of the project """

    def local_read_fn(x: any = None):
        if project.now_testing:
            """ for pytest """
            return lambda x: mock_read(x)
        """for production"""
        return lambda x: Read(x)

    if project.version_file_path.is_file():
        c = local_read_fn()(project.version_file_path)
        c = c.replace("version", "")
        c = c.replace("=", "").strip()
        print(c, "xx")
    else:
        if not project.now_testing:
            print(project.version_file_path, "not a file ")
            check_and_write(project, project.default_version)
            return project.default_version
            # raise VersionNotFound(project.version_file_path)
    return c


def get_prev_version_instance(project: Project):
    """get_prev_version_instance """
    previous_version = project.default_version
    try:
        previous_version = get_previous(project)
    except  VersionNotFound:
        ...
        previous_version = project.default_version
        # raise "could not read"
        # previous_version = project.default_version
    except Exception as exc:
        print(exc)
        previous_version = project.default_version
    return create_version_instance(previous_version, project)


def get_current_version_instance(project: Project):
    """get_prev_version_instance """
    previous_version = project.default_version
    try:
        previous_version = get_previous(project)
    except  VersionNotFound:
        ...
        previous_version = project.default_version
        # raise "could not read"
        # previous_version = project.default_version
    except Exception as exc:
        print(exc)
        previous_version = project.default_version
    return create_version_instance(previous_version, project)


def check_and_write(project: t.Union[Project, str], version: str):
    """check_and_write create version file __version__.py"""
    from ..components.increment_functions import get_project_from_package_name
    if isinstance(project, str):
        project = get_project_from_package_name(project)

    print(version, "writing version")
    try:
        Write(project.version_file_path, f"#{version}")
        print(f"version file was created...\n  {project.version_file_path} : project.next_version")
    except Exception as exc:

        print(f"{exc} ==>version file was not created...\n  {project.version_file_path} : project.next_version")


# ---------------------------------------------------------------------
#               M A I N
# ---------------------------------------------------------------------
def get_next_version(project: Project = Project(),
                     increment_=True,
                     prerelease=True,
                     verbose=True,
                     write_version_file=True,
                     now_testing=False,
                     ) -> VersionParts:
    """
    gets current version of the project and increments depending on arguments given by developer...
        @params
            project : Project => see Project class which takes path to version file
            ------------
            increment_ : bool => it may increment or return same version
            ------------
                if True => depending on prerelease parameter creates new version number
                if False => ignores prerelease parameter and just returns current version
            prerelease : bool => creates next version by incrementin and adding "rc" text to the version
            ------------
                    (lets suppose current version is 0.0.1.2)
                if True => creates a version like 0.0.1.3rc1
                if False =>  creates a version like 0.0.1.3
            verbose : bool
            ------------
                verbose or silent while doing process
            write_version_file :  pathlib.Path  or str
            ------------
                if True : writes new version to given path
                if False : does not write any file
            now_testing: bool => default : False
            ------------
                for testing purposes it plays with fake versions
                this will be set True while testing development
    """
    from verser.verserLocal.components.increment_functions import increment_version
    if now_testing:
        project.now_testing = now_testing
    if project.now_testing:
        now_testing = project.now_testing
    prev_instance = get_prev_version_instance(project)
    project.version = prev_instance
    if not increment_:
        next_instance = prev_instance
    else:
        next_instance = increment_version(prev_instance, part="patch")
    if verbose:
        print("-" * 15)
        print("CURRENT VERSION", prev_instance)
        print(f"increment : {increment_}")
        print(f"prerelease : {prerelease}")
        if prev_instance.version != next_instance:
            print("VERSION number was incremented...")
        print("NEW VERSION", next_instance)
    project.next_version = next_instance
    if write_version_file:
        """ write new version"""
        if write_version_file:
            check_and_write(project, str(project.next_version))
    return next_instance


def get_current_version(project: Project = Project(),
                        verbose=True,
                        write_version_file=True,
                        now_testing=False,
                        ) -> VersionParts:
    """
    get_current_version
    Read-only function
        tries to find out current version of the file and returns.
        @params
            project : Project => see Project class which takes path to version file
            verbose : bool
                verbose or silent while doing process
            write_version_file :  pathlib.Path  or str
                if True : writes new version to given path
                if False : does not write any file
            test :
                for testing purposes it plays with fake versions
    """
    prev_instance = get_prev_version_instance(project)
    project.version = prev_instance
    if verbose:
        print(project.version.info)

    if write_version_file:
        """ write current version"""
        check_and_write(project, str(project.version))

    return prev_instance
