"""Get a list of packages with package compatibility.
"""
from __future__ import annotations

from os import path

import requirements

from licensecheck import packageinfo
from licensecheck.types import UNKNOWN, PackageInfo, RequirementInfo


def getReqs(files: list) -> set[RequirementInfo]:
    """Get requirements for the end user project/ lib.

    >>> getReqs([/api/requirements.txt, requirements-dev.txt]])

    Args:
        files (list)

    Returns:
        set[RequirementInfo]: Set of requirement info.
    """
    reqs = set()

    # Requirements
    for file in files:
        with open(file, encoding="utf-8") as requirementsTxt:
            for req in requirements.parse(requirementsTxt):
                version = UNKNOWN
                for spec in req.specs:
                    if spec[0] == "==":
                        version = spec[1]

                reqs.add(
                    RequirementInfo(
                        name=req.name,
                        version=version,
                        filename=file,
                        dir=path.basename(path.dirname(path.abspath(file))),
                    )
                )
    return reqs


def getDepsWithLicenses(files: list) -> set[PackageInfo]:
    """Get a set of dependencies with licenses and determine license compatibility.

    Args:
        files (list): List of requirements.txt files. e.g. [/api/requirements.txt, requirements-dev.txt]

    Returns:
        set[PackageInfo]: tuple of my package license
    """
    reqs = getReqs(files)

    # Get info about packages
    packages = packageinfo.getPackages(reqs)

    return packages
