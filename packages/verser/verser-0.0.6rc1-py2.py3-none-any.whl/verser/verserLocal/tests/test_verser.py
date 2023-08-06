from pathlib import Path

from verser.verserLocal.components.increment_functions import increment_version_pypi
from verser.verserLocal.components.version_functions import get_current_version, get_next_version
from verser.verserLocal.components.project import Project
from verser.verserLocal.verser_ import *

import random




def test_get_next_version(capsys):
    for item in range(3):
        inc = random.choice((True, False,))
        # inc = True
        pre = random.choice((True, False,))
        n = get_next_version(project=Project(version_file_path=Path("verser"),
                                             now_testing=True),
                             increment_=inc,
                             prerelease=pre,
                             verbose=True)
        # assert n is not None
        with capsys.disabled():
            n = get_next_version(
                project=Project(now_testing=True),
                increment_=inc,
                prerelease=pre,
                verbose=True
            )
            # assert n is not None


def test_get_current_version(capsys):
    for item in range(3):
        # inc = random.choice((True, False,))
        inc = True
        pre = random.choice((True, False,))
        # n = get_current_version(project=Project(), increment_=inc, pre_release=pre, verbose=True)
        # assert n is not None
        with capsys.disabled():
            n = get_current_version(project=Project(now_testing=True),
                                    verbose=True,
                                    now_testing=True
                                    )

            # assert n is not None

def test_examples(capsys):
    with capsys.disabled():
        some_examples_instances_from_string()
        some_examples_instances_from_tuple()


def test_increment_version_pypi(capsys):

    with capsys.disabled():
        nv = increment_version_pypi(package_name="rich")
        print(nv)



