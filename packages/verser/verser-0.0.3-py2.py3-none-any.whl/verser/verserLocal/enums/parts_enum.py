from enum import Enum, auto
import typing as t

from enum import Enum, auto


class VersionPartEnum(Enum):
    major = auto()
    minor = auto()
    patch = auto()
    pre = auto()
    build = auto()


major = VersionPartEnum.major.value
minor = VersionPartEnum.minor.value
patch = VersionPartEnum.patch.value
pre = VersionPartEnum.pre.value
build = VersionPartEnum.build.value


def get_enum_with_value(
        key: t.Union[Enum, str, int],
        enum_: t.Union[str, int, t.Callable, Enum],
        # enum_: Enum,
        default_value: t.Union[str, int, t.Callable, Enum] = None

) -> Enum:
    """

    :rtype: object
    """
    if isinstance(key, Enum):
        return key
    if isinstance(key, int):
        key = str(key)

    if hasattr(default_value, "value"):
        """otherwise probably None """
        default_value = getattr(default_value, "value", None)

    dd = {str(x.value): x for x in enum_}
    enum_value: Enum = dd.get(key, None)

    if hasattr(enum_value, "value"):
        v = getattr(enum_value, "value")
        return v
    if not default_value:
        return getattr(default_value, "default")
    return default_value
# ------------------------------------------------------- / get_enum_with_value -------------------------------------------------------
