# Using regular expresion they provided we are going to check validity nad get parts
import re
import typing as t
from rich import inspect

from verser.verserLocal.components.version_parts import VersionParts


def valid_check(version_str: str):
    if isinstance(version_str, VersionParts):
        version_str = str(VersionParts)

    if not isinstance(version_str, str):
        print(f"valid_check has to get string {valid_check}")
        return False

    r = "^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    matches = re.match(r, version_str)
    inspect(matches)
    return matches


def get_parts_from_version_string(version_str: str):
    v = valid_check(version_str)
    if not v:
        return False
    return v["major"], v["minor"], v["patch"], v["prerelease"], v["buildmetadata"]


"""
verser will implement versions below if user wants to increment current version

1.0.0-rc.1+build.1
2.0.0-rc.1+build.123
('1', '0', '0', 'rc.1', 'build.1')
('2', '0', '0', 'rc.1', 'build.123')

1.0.0
2.0.0
1.1.7
2.0.0+build.1848
2.0.1-alpha.1227

"""

# Reference to valuable source of information here.
# https://semver.org/
# https://regex101.com/r/Ly7O1x/3
"""Valid Semantic Versions
"""
valid_format_examples = f"""
0.0.4
1.2.3
10.20.30
1.1.2-prerelease+meta
1.1.2+meta
1.1.2+meta-valid
1.0.0-alpha
1.0.0-beta
1.0.0-alpha.beta
1.0.0-alpha.beta.1
1.0.0-alpha.1
1.0.0-alpha0.valid
1.0.0-alpha.0valid
1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay
1.0.0-rc.1+build.1
2.0.0-rc.1+build.123
1.2.3-beta
10.2.3-DEV-SNAPSHOT
1.2.3-SNAPSHOT-123
1.0.0
2.0.0
1.1.7
2.0.0+build.1848
2.0.1-alpha.1227
1.0.0-alpha+beta
1.2.3----RC-SNAPSHOT.12.9.1--.12+788
1.2.3----R-S.12.9.1--.12+meta
1.2.3----RC-SNAPSHOT.12.9.1--.12
1.0.0+0.build.1-rc.10000aaa-kk-0.1
99999999999999999999999.999999999999999999.99999999999999999
"""

"""Invalid Semantic Versions
"""
invalid_format_examples = f"""
1
1.2
1.2.3-0123
1.2.3-0123.0123
1.1.2+.123
+invalid
-invalid
-invalid+invalid
-invalid.01
alpha
alpha.beta
alpha.beta.1
alpha.1
alpha+beta
alpha_beta
alpha.
alpha..
beta
1.0.0-alpha_beta
-alpha.
1.0.0-alpha..
1.0.0-alpha..1
1.0.0-alpha...1
1.0.0-alpha....1
1.0.0-alpha.....1
1.0.0-alpha......1
1.0.0-alpha.......1
01.1.1
1.01.1
1.1.01
1.2
1.2.3.DEV
1.2-SNAPSHOT
1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788
1.2-RC-SNAPSHOT
-1.0.3-gamma+b7718
+justmeta
9.8.7+meta+meta
9.8.7-whatever+meta+meta
99999999999999999999999.999999999999999999.99999999999999999----RC-SNAPSHOT.12.09.1--------------------------------..12
"""


def get_some_example_version_tuples():
    for item in valid_format_examples.splitlines():
        print(get_parts_from_version_string(item.strip()))
        yield get_parts_from_version_string(item.strip())


def get_some_example_version_string():
    for item in valid_format_examples.splitlines():
        yield item.strip()

# nottest_some_instances()
