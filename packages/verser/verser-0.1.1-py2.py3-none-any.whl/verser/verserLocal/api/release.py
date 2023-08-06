import json

from dataclasses import dataclass

from verser.verserLocal.components.version_parts import VersionParts


# -----------------------------------------    -------------------------------------
@dataclass
class Release:
    version_text: str
    version: VersionParts
    date: str
    yanked: False
    raw: dict


# -----------------------------------------    -------------------------------------


def create_class_release(key, result_dict, verbose=False):
    from verser.verserLocal.components.version_functions import create_version_instance
    if not result_dict:
        return False

    obj1 = result_dict.get(key, None)
    if not obj1:
        return False
    obj = obj1[0]

    vp = create_version_instance(key, verbose=verbose)
    return Release(
        version_text=key,
        version=vp,
        date=obj["upload_time"],
        yanked=obj["yanked"],
        raw=obj,

    )


def populate_releases(result_dict: dict):
    keys = list(result_dict["releases"].keys())
    releases = tuple(create_class_release(x, result_dict["releases"]) for x in keys)
    releases = tuple(x for x in releases if x)
    return sorted(releases, key=lambda x: x.version.value, reverse=True)


def populate_releases_early(result_dict: dict):
    keys = list(result_dict["releases"].keys())
    releases = tuple(create_class_release(x, result_dict["releases"]) for x in keys)
    versions = tuple(x.version for x in releases)
    return sorted(versions, key=lambda x: x.value, reverse=True)


def get_releases_with_reversed_sort(result_dict: dict):
    return populate_releases(result_dict)


def get_latest_version_of_vers(result_dict: dict):
    return populate_releases(result_dict)[0]
