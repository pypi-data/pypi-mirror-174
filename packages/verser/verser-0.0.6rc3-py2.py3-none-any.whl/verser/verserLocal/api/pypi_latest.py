# from verser.verserLocal.requests_.requests_ import get_request_with_no_cache
from verser.verserLocal.api.release import populate_releases, get_latest_version_of_vers, \
    get_releases_with_reversed_sort
from verser.verserLocal.requests_.requests_ import get_request_with_cache, get_request_without_cache
from dataclasses import dataclass
from verser.verserLocal.common.colors import *

# sources = ('https://img.shields.io/pypi/v/', 'https://pypi.org/pypi/evdspy/json')

from abc import ABC
from rich import inspect


@dataclass
class UrlFormat():
    package_name: str
    url: str = ''

    def format(self):
        pass


@dataclass
class UrlFormatPYPI(UrlFormat):
    url: str = 'https://pypi.org/pypi/verser/json/'

    def format(self):
        self.url = f'https://pypi.org/pypi/{self.package_name}/json'
        return self.url


development = False
import typing as t

sources: t.Tuple[any] = (UrlFormatPYPI,)

import requests


def get_response(package_name: str):
    for source in sources:
        s = source(package_name)
        url = s.format()
        # url = source(package_name).url
        print(url)
        if development:
            result = get_request_with_cache(url)
        else:
            result = get_request_without_cache(url)

        import json
        if result and isinstance(result, requests.models.Response):
            result_dict = json.loads(result.text)
            # populate_releases(result_dict )
            return result_dict  # get_latest_version_of_vers(result_dict), result_dict
        return False


def get_latest_version(package_name: str):
    """
    :type package_name: str
    """
    releases = get_all_releases(package_name)
    if not releases:
        print(f"package info not found version info for the package `{package_name}`")
        return

    if releases:
        return releases[0]

    return "not found"


def get_all_releases(package_name: str):
    """

    :type package_name: str
    """
    result_dict = get_response(package_name)
    if not check_response(result_dict):
        return
    if result_dict and "releases" in result_dict:
        releases = get_releases_with_reversed_sort(result_dict)
        # print(releases)
        # print(releases.keys())
        return releases
    return False


def check_response(releases):
    if not releases:
        print(f"program could not found any version info for the package `{package_name}`")
        return False
    return True


def display_all_versions(package_name: str):
    releases = get_all_releases(package_name)
    if not check_response(releases):
        return
    msg = "\n".join((x.version_text for x in releases))
    print(msg)


def display_columns(releases, columns):
    def display_column(item, column):
        if column in item:
            ...


def releases(package_name: str):
    releases = get_all_releases(package_name)
    print(releases, "\nreleases")


def last_version(package_name: str):
    v = get_latest_version(package_name)
    print(v)


package_name = "menu"

# # releases()
# last_version(package_name)
#
# display_all_versions(package_name)

from verser.verserLocal.format.format_check import valid_check
# v= valid_check("15.14.22-rc1")
# print(v["major"])
# print(v["minor"])
# print(v["patch"])
# print(v["prerelease"])
# print(v["buildmetadata"])

# inspect(v , all= True )
# print(valid_check("1.2.2"))
# print(valid_check("1.2+2"))
