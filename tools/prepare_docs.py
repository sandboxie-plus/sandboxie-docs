#!/usr/bin/env python3
"""Prepare the publishing language layout in a new, isolated build directory."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import stat
import sys


def _overlaps(first: Path, second: Path) -> bool:
    return first == second or first in second.parents or second in first.parents


def _check_unlinked_tree(root: Path) -> None:
    """Do not follow source links, including Windows directory junctions."""
    paths = [root]
    while paths:
        path = paths.pop()
        info = path.lstat()
        is_reparse_point = getattr(info, "st_file_attributes", 0) & 0x400
        if stat.S_ISLNK(info.st_mode) or is_reparse_point:
            raise ValueError(f"source links are not supported: {path}")
        if stat.S_ISDIR(info.st_mode):
            paths.extend(path.iterdir())
        elif not stat.S_ISREG(info.st_mode):
            raise ValueError(f"source is not a regular file or directory: {path}")


def prepare_docs(repo: Path, output: Path) -> tuple[Path, int]:
    """Copy build inputs and return the build root and number of fallback pages.

    The output must not exist and must be outside the source repository. Only
    top-level Markdown pages in Content and PlusContent receive English
    fallbacks, matching the publishing workflow's existing preparation step.
    """
    repo = repo.resolve(strict=True)
    output_arg = output.absolute()
    if os.path.lexists(output_arg):
        raise ValueError(f"output already exists; choose a new directory: {output_arg}")
    output = output_arg.resolve()
    if _overlaps(repo, output):
        raise ValueError("output must be outside the repository and must not contain it")

    docs = repo / "docs"
    material = repo / "material"
    config = repo / "mkdocs.yml"
    for directory in (docs, material, docs / "zh-CN"):
        if not directory.is_dir():
            raise ValueError(f"required source directory is missing: {directory}")
    if not config.is_file():
        raise ValueError(f"required source file is missing: {config}")
    for source in (docs, material, config):
        _check_unlinked_tree(source)

    output.mkdir(parents=True, exist_ok=False)

    def skip_generated_language(directory: str, names: list[str]) -> list[str]:
        return ["zh"] if Path(directory) == docs and "zh" in names else []

    shutil.copytree(docs, output / "docs", ignore=skip_generated_language)
    shutil.copytree(material, output / "material")
    shutil.copy2(config, output / "mkdocs.yml")

    prepared_docs = output / "docs"
    chinese = prepared_docs / "zh-CN"
    fallback_count = 0
    for name in ("Content", "PlusContent"):
        source = prepared_docs / name
        target = chinese / name
        target.mkdir(parents=True, exist_ok=True)
        for page in sorted(source.glob("*.md")):
            destination = target / page.name
            if page.is_file() and not destination.exists():
                shutil.copy2(page, destination)
                fallback_count += 1

    shutil.copytree(chinese, prepared_docs / "zh")
    (output / ".prepared-docs").write_text("sandboxie-docs-prepared-v1\n", encoding="utf-8")
    return output, fallback_count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="source repository root")
    parser.add_argument("--output", type=Path, required=True, help="new build directory outside the repository")
    args = parser.parse_args(argv)
    try:
        output, fallback_count = prepare_docs(args.repo, args.output)
    except (OSError, RuntimeError, ValueError) as error:
        print(f"prepare_docs: {error}", file=sys.stderr)
        return 2
    print(f"Prepared documentation in {output} ({fallback_count} English fallback pages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
