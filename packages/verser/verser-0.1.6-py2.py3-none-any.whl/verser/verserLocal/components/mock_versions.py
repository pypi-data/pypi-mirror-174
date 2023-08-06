import random
# ------------------------------------------- () mock_versions

# test = False
mock_versions = {
    0: "1.0.17",
    1: "1.0.17-3rc2",
    2: "1.0.17-8rc6",
    3: "1.0.17.7",
    4: "1.0.17.9rc2",
    5: "1.0.17.9rc8",
}
"""

1.0.0-rc.1+build.1
2.0.0-rc.1+build.123
1.0.0-alpha
1.0.0-beta
"""
mock_versions_old = {
    0: "1.0.17.2",
    1: "1.0.17.3rc2",
    2: "1.0.17.8rc6",
    3: "1.0.17.7",
    4: "1.0.17.9rc2",
    5: "1.0.17.9rc8",
}


# ------------------------------------------- (fnc) mock_read

def mock_read(*args, **kwargs) -> str:
    x = random.choice(tuple(mock_versions.keys()))
    return mock_versions[x]

