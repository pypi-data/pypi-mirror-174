from verser.verserLocal.components.version_parts import VersionParts


def display_version(v: VersionParts):
    if not v:
        return
    msg = f"""
-----------------------------------------------------------------
original version (str) : {v.original}
version : {v.version}
value : {v.value}
str : {v.version}
{v.info}
"""
    print(msg)
    return msg
