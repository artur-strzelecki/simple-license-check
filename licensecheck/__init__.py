"""Output the licenses from requirements.txt files."""
from __future__ import annotations

import argparse
from sys import stdout

from licensecheck import formatter, get_deps

stdout.reconfigure(encoding="utf-8")


def cli() -> None:
    """Cli entry point."""
    parser = argparse.ArgumentParser(description=__doc__, argument_default=argparse.SUPPRESS)
    parser.add_argument(
        "--output-format",
        help=f"Output format. one of: {', '.join(list(formatter.formatMap))}. default=simple",
        default="simple",
    )
    parser.add_argument(
        "--output-file",
        help="Filename to write to (omit for stdout).",
    )
    parser.add_argument(
        "--requirements-files",
        help="Requirements files to check. default=requirements.txt",
        nargs="+",
        default=["requirements.txt"],
    )
    args = vars(parser.parse_args())

    # File
    filename = (
        stdout
        if args.get("output_file") is None
        else open(args["output_file"], "w", encoding="utf-8")
    )

    # Get list of licenses
    depsWithLicenses = get_deps.getDepsWithLicenses(args.get("requirements_files"))

    # Format the results
    if args["output_format"] in formatter.formatMap:
        print(
            formatter.formatMap[args["output_format"]](
                sorted(depsWithLicenses, key=lambda dep: (dep.requirement.dir, dep.name))
            ),
            file=filename,
        )

    # Cleanup
    filename.close()
