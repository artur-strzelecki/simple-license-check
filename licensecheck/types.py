"""PackageCompat type.
"""
from __future__ import annotations

from dataclasses import dataclass, field

UNKNOWN = "UNKNOWN"
JOINS = ";; "


@dataclass(unsafe_hash=True, order=True)
class PackageInfo:
    """PackageInfo type."""

    name: str
    requirement: RequirementInfo
    version: str = UNKNOWN
    namever: str = field(init=False)
    size: int = -1
    homePage: str = UNKNOWN
    author: str = UNKNOWN
    license: str = UNKNOWN
    errorCode: int = 0

    def __post_init__(self):
        self.namever = f"{self.name}-{self.version}"


@dataclass(unsafe_hash=True, order=True)
class RequirementInfo:
    name: str
    filename: str
    dir: str
    version: str = UNKNOWN

    def to_url(self) -> str:
        if self.version != UNKNOWN:
            return f"{self.name}/{self.version}"

        return f"{self.name}"
