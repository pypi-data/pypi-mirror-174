from dataclasses import dataclass


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch
