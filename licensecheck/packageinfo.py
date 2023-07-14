"""Get information for installed and online packages.
"""
from __future__ import annotations

import requests

from licensecheck.types import JOINS, UNKNOWN, PackageInfo, RequirementInfo


def getPackageInfoPypi(requirement: RequirementInfo) -> PackageInfo:
    """Get package info from local files including version, author
    and the license.

    :param RequirementInfo requirement: RequirementInfo instance
    :raises ModuleNotFoundError: if the package does not exist
    :return PackageInfo: package information
    """

    request = requests.get(f"https://pypi.org/pypi/{requirement.to_url()}/json", timeout=60)
    response = request.json()
    try:
        info = response["info"]
        licenseClassifier = licenseFromClassifierlist(info["classifiers"])
        return PackageInfo(
            name=requirement.name,
            requirement=requirement,
            version=info["version"],
            homePage=info["home_page"],
            author=info["author"],
            size=int(response["urls"][-1]["size"]),
            license=licenseClassifier if licenseClassifier != UNKNOWN else info["license"],
        )
    except KeyError as error:
        raise ModuleNotFoundError from error


def licenseFromClassifierlist(classifiers: list[str]) -> str:
    """Get license string from a list of project classifiers.

    Args:
        classifiers (list[str]): list of classifiers

    Returns:
        str: the license name
    """
    if not classifiers:
        return UNKNOWN
    licenses = []
    for val in classifiers:
        if val.startswith("License"):
            lice = val.split(" :: ")[-1]
            if lice != "OSI Approved":
                licenses.append(lice)
    return JOINS.join(licenses) if len(licenses) > 0 else UNKNOWN


def getPackages(reqs: set[tuple[str, str | None]]) -> set[PackageInfo]:
    """Get dependency info.

    Args:
        reqs (set[str]): set of dependency names to gather info on

    Returns:
        set[PackageInfo]: set of dependencies
    """
    packageinfo = set()
    for requirement in reqs:
        try:
            packageinfo.add(getPackageInfoPypi(requirement))
        except ModuleNotFoundError:
            packageinfo.add(
                PackageInfo(name=requirement.name, requirement=requirement, errorCode=1)
            )

    return packageinfo
