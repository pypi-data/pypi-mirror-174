from dataclasses import dataclass
from pathlib import Path

from modulepy import MODULE_BASE_DIRECTORY
from modulepy.Version import Version


@dataclass
class Information:
    name: str
    version: Version

    def __str__(self):
        return f"{self.name} {self.version}"

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version

    def get_directory(self):
        return MODULE_BASE_DIRECTORY / self.name

    def get_address(self) -> Path:
        return self.get_directory() / (self.name + ".sock")

    def is_available(self, modules: list[str]) -> bool:
        """
        checks if the str representation is in the modules list
        :param modules:
        :return:
        """
        return self.name in modules
