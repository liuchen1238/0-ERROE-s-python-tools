#!/usr/bin/env python3
"""
pip_module_manager
===================

This script provides a simple command‑line interface for managing Python
packages installed via ``pip``. It offers two primary features:

* **List installed packages**: shows all packages currently available in the
environment along with their versions.
* **Download packages**: fetches distribution archives of a package from
  PyPI without installing it. The downloads are stored in a chosen output
directory.

Usage examples::

    # List all installed packages
    python pip_module_manager.py list

    # Download the latest version of ``requests`` into the current directory
    python pip_module_manager.py download requests

    # Download ``numpy`` into a specific folder
    python pip_module_manager.py download numpy --dir /tmp/downloads

The script is intentionally modular: the core functionality is broken into
functions that can be reused in other programs or imported as a module.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Tuple

try:
    # Python 3.8+: use importlib.metadata for installed distributions
    from importlib import metadata as importlib_metadata  # type: ignore
except ImportError:
    # Fallback for older Python versions
    import importlib_metadata  # type: ignore  # type: ignore[no-redef]


def get_installed_packages() -> Iterable[Tuple[str, str]]:
    """Return an iterable of (name, version) for installed distributions.

    Uses ``importlib.metadata`` when available. This avoids invoking ``pip``
    and remains a lightweight way of inspecting the current environment.

    Yields:
        Tuples of package name and version, sorted alphabetically by name.
    """
    distributions = importlib_metadata.distributions()
    # Some distributions may not have a proper ``Name`` field; skip those
    packages: list[Tuple[str, str]] = []
    for dist in distributions:
        metadata = dist.metadata
        name = metadata.get("Name") or metadata.get("name")
        version = metadata.get("Version") or metadata.get("version")
        if name and version:
            packages.append((name, version))
    return sorted(packages, key=lambda x: x[0].lower())


def list_installed_packages() -> None:
    """Print a list of installed packages to stdout.

    Each package is displayed on its own line in ``name==version`` format.
    """
    for name, version in get_installed_packages():
        print(f"{name}=={version}")


def download_package(package: str, output_dir: Path) -> None:
    """Download a package from PyPI using ``pip download``.

    Args:
        package: The name of the package (optionally with version specifier)
            to download. Example: ``'requests==2.31.0'``.
        output_dir: Directory where the distribution files should be stored.

    This function invokes ``pip`` as a subprocess to ensure correct handling
    of package resolution, caching and network access. Any output from the
    subprocess is printed to stdout/stderr accordingly. If ``pip`` exits
    with a non‑zero status, a ``SystemExit`` is raised.
    """
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "pip", "download", package, "--dest", str(output_dir)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        # Print pip's stderr to the user's stderr and exit with the same code
        print(exc.stderr, file=sys.stderr)
        raise SystemExit(exc.returncode)
    # Print pip's stdout to inform the user of downloaded files
    print(result.stdout)


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments for this tool.

    Supports two subcommands: ``list`` and ``download``.

    Args:
        argv: List of command line arguments; defaults to ``sys.argv[1:]``.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Manage pip packages: list installed packages or download packages "
            "from PyPI without installing them."
        )
    )
    subparsers = parser.add_subparsers(title="commands", dest="command", required=True)

    # 'list' subcommand
    parser_list = subparsers.add_parser("list", help="List installed pip packages")
    parser_list.set_defaults(func=lambda args: list_installed_packages())

    # 'download' subcommand
    parser_download = subparsers.add_parser("download", help="Download a package from PyPI")
    parser_download.add_argument(
        "package",
        help=(
            "The package name to download (optionally with version specifier, e.g., "
            "'requests==2.31.0')."
        ),
    )
    parser_download.add_argument(
        "-d",
        "--dir",
        dest="dir",
        type=Path,
        default=Path.cwd(),
        help="Destination directory where downloaded files will be stored (default: current working directory)",
    )
    parser_download.set_defaults(func=lambda args: download_package(args.package, args.dir))

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Entry point for the CLI.

    This function delegates to the appropriate handler based on the chosen
    subcommand. It also catches ``SystemExit`` raised by ``download_package``
    when ``pip`` encounters an error, re‑raising it after printing a user‑friendly
    message.
    """
    args = parse_arguments(argv)
    try:
        args.func(args)
    except SystemExit as exc:
        # Provide context for pip errors
        print(f"pip exited with status {exc.code}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
