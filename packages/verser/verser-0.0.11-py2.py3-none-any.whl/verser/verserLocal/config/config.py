from ..utils.utils_general import *
from ..common.files import Read
from ..common.colors import *
from ..state.current_state import *
from ..state.test_or_real import check_if_this_is_pytest


def get_develop_vers_main():
    parent = Path(__file__).parent
    v = Read(Path(parent / ".." / ".." / "__version__.py"))
    if isinstance(v , str ) :
        v = v.replace("#" , "")
    return v


def version_raw():
    v = get_develop_vers_main()
    return v


def version_display():
    v = get_develop_vers_main()
    import site
    s = site.getsitepackages()
    site_pack = ""
    f = ""
    if len(s) > 1:
        site_pack = s[1]
        f = "from"
    # print_with_success_style(f"evdspy {v} {f} ")
    # print_with_info_style(f"evdspy {v} {f} {site_pack}")
    v = f"evdspy {v} {f} {site_pack}"
    print_with_info_style(v)

from dataclasses import dataclass
from abc import ABC


@dataclass
class ConfigBase(ABC):
    cancel_request_temp: bool = False
    current_mode_is_test: bool = check_if_this_is_pytest()
    projectName: str = 'verser'
    interiorFolder = 'verserLocal'
    runtime_file_name_root_path = get_current_dir() / '..'
    # runtime_file_name_path = get_current_dir() / '..' / "components" / "options.py"
    # user_options_file_name = Path.cwd() / 'IO' / 'options.py'
    # user_options_file_name_locked = Path.cwd() / 'IO' / 'options-locked.py'
    version: str = version_raw()

    def version_display(self):
        version_display()


config = ConfigBase()

__all__ = [
    'ConfigBase',
    'config'
]
