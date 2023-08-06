# ------------------------------------------- (Class) Project
from dataclasses import dataclass
import typing as t
from .defaults import DEFAULT_START_VERSION
from pathlib import Path

from .version_parts import VersionParts


@dataclass
class Project():
    """Project"""
    package_name: str = "XYZ"
    default_version: str = DEFAULT_START_VERSION
    version_file_path: t.Union[str, Path] = '__version__.py'
    now_testing: bool = False
    version: VersionParts = None
    next_version: VersionParts = None
    """
    Project (Class)
    @attrs
        package_name: str => package name  
        ------------
        default_version: str  => 
        ------------
            if there is not a version file yet this will be used to start a version number 
            default is : 0.0.0.0    
                    (when incremented with function below it will be 0.0.0.1 or 0.0.0.1rc1 )

        version_file_path: Union[str, Path] => 
        ------------
            Version file address : this will be used to read current version  

        now_testing: bool => default : False 
        ------------
            this will be set True while testing development 

    """

    def __post_init__(self):
        if isinstance(self.version_file_path, str):
            self.version_file_path = Path(self.version_file_path)
