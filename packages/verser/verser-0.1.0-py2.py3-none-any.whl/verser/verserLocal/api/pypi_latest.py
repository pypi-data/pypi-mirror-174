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
    if not check_response(result_dict , package_name):
        return
    if result_dict and "releases" in result_dict:
        releases = get_releases_with_reversed_sort(result_dict)

        return releases
    return False


def check_response(releases , package_name):
    if not releases:
        print(f"program could not found any version info for the package : {package_name} ")
        return False
    return True


def display_all_versions(package_name: str):
    releases = get_all_releases(package_name)
    if not check_response(releases , package_name ):
        return
    msg = "\n".join((x.version_text for x in releases))


def display_columns(releases, columns):
    def display_column(item, column):
        if column in item:
            ...


def releases(package_name: str):
    releases = get_all_releases(package_name)


def last_version(package_name: str):
    v = get_latest_version(package_name)
