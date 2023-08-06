from verser.verserLocal.components.version_functions import (
    display_version,
    create_version_instance
)
from verser.verserLocal.components.increment_functions import increment_version
from verser.verserLocal.components.version_parts import VersionParts
from verser.verserLocal.format.format_check import get_some_example_version_tuples, get_some_example_version_string



from rich import inspect


def some_examples_instances_from_tuple():
    for item in get_some_example_version_tuples():
        print(f"item : {item}")
        if item:
            if isinstance(item, tuple):
                v = VersionParts(*item)
                display_version(v)


def some_examples_instances_from_string():
    for item in get_some_example_version_string():
        print(f"item : {item}")
        if item:
            if isinstance(item, str):
                v = create_version_instance(item)
                display_version(v)
                print("-increment-" * 15)
                v2 = increment_version(v)
                display_version(v2)
