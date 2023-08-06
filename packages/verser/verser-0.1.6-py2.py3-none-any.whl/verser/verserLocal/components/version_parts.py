# ------------------------------------------ (Class) VersionParts
from dataclasses import dataclass
import re
import typing as t


@dataclass
class VersionParts:
    major: str
    minor: str
    patch: str
    prerelease: str = ""
    buildmetadata: str = ""
    major_num: int = 0
    minor_num: int = 0
    patch_num: int = 0
    prerelease_num: int = 0
    buildmetadata_num: int = 0
    version = ""
    value = 0
    original: str = ""
    original_tuple = False

    def convert_int(self, item):
        if not item:
            return 0
        if isinstance(item, str):
            if re.findall(r'\d+', item):  # str(item).isalnum():
                new_item = re.sub('[^0-9]', '', item)
                return int(new_item)

            numbers = re.findall(r'\d+', item)
            # [1rc2ra] => [1, 2]
            if len(numbers) == 2:
                return numbers[0] * 100 + numbers[1] * 1
            if len(numbers) == 1:
                return numbers[0] * 100

            if len(numbers) == 0:
                return 0
            return 0
        return 0

    def __post_init__(self):
        # 2.0.0-rc.1+build.123
        # self.original= self.version

        items = ("major", "minor", "patch", "prerelease", "buildmetadata")
        for item in items:
            setattr(self, f"{item}_num", self.convert_int(getattr(self, item)))
        self.combine()

        self.value = self.major_num * 10 ** 8 + self.minor_num * 10 ** 6 + self.patch_num * 10 ** 4 + self.buildmetadata_num * 10 ** 2
        if self.prerelease:
            self.value += (10 ** 4) * -1 + self.convert_int(self.prerelease_num)

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def combine(self):
        if self.prerelease_num and self.buildmetadata_num:

            self.version = f"{self.major}.{self.minor}.{self.patch}rc{self.prerelease_num}.dev{self.buildmetadata_num}"

        if self.prerelease_num and not self.buildmetadata_num:
            self.version = f"{self.major}.{self.minor}.{self.patch}rc{self.prerelease_num}"
        if not self.prerelease_num and self.buildmetadata_num:
            # 2.0.0-rc.1+build.123
            self.version = f"{self.major}.{self.minor}.{self.patch}.dev{self.buildmetadata_num}"
        if not self.prerelease_num and not self.buildmetadata_num:
            self.version = f"{self.major}.{self.minor}.{self.patch}"

    def __str__(self):
        return self.version

    @property
    def info(self):
        msg = f"""
major : {self.major}
minor : {self.minor}
patch : {self.patch}
prerelease : {self.prerelease}
buildmetadata : {self.buildmetadata}
"""
        return msg
