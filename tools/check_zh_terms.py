#!/usr/bin/env python3
"""Check added Simplified Chinese documentation lines for deprecated terms."""

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys


# Match manager names first so their shorter 'sandbox' terms are not reported twice.
TERMS = re.compile("沙[盘盒箱]管理器|沙箱|沙盘")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


@dataclass(frozen=True)
class Violation:
    path: str
    line: int
    term: str

    @property
    def severity(self) -> str:
        return "warning" if self.term.endswith("管理器") else "error"

    @property
    def message(self) -> str:
        if self.severity == "warning":
            return (
                f"Check '{self.term}' in context: use 'SandMan' for the Sandboxie Plus UI "
                "or 'Sandboxie Control' for the Classic UI. Exact UI label quotations may be kept."
            )
        return f"Use '沙盒' instead of '{self.term}' in Simplified Chinese documentation."


def git(repo: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "--literal-pathspecs", *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return result.stdout.decode("utf-8")
    except subprocess.CalledProcessError as error:
        raise RuntimeError(error.stderr.decode("utf-8", errors="replace").strip()) from error
    except (OSError, UnicodeDecodeError) as error:
        raise RuntimeError(str(error)) from error


def is_target(path: str) -> bool:
    return path == "README_zh-CN.md" or (
        path.startswith("docs/zh-CN/") and path.endswith(".md")
    )


def added_terms(path: str, patch: str) -> list[Violation]:
    violations = []
    new_line = 0
    remaining = 0
    for line in patch.split("\n"):
        match = HUNK.match(line)
        if match:
            new_line = int(match[1])
            remaining = int(match[2]) if match[2] is not None else 1
        elif remaining and line.startswith("+"):
            # Inside a hunk, even a line starting with '+++' is document text.
            for term in sorted(set(TERMS.findall(line[1:]))):
                violations.append(Violation(path, new_line, term))
            new_line += 1
            remaining -= 1
        elif remaining and line.startswith(" "):
            new_line += 1
            remaining -= 1
    return violations


def check(repo: Path, base: str, head: str = "HEAD") -> list[Violation]:
    base_sha = git(repo, "rev-parse", "--verify", "--end-of-options", f"{base}^{{commit}}").strip()
    head_sha = git(repo, "rev-parse", "--verify", "--end-of-options", f"{head}^{{commit}}").strip()
    start = git(repo, "merge-base", base_sha, head_sha).strip()
    diff_options = ["--no-ext-diff", "--no-textconv", "--no-renames"]
    # NUL delimiters preserve spaces, Unicode and other special path characters.
    names = git(
        repo, "diff", *diff_options, "--name-only", "-z", "--diff-filter=d",
        start, head_sha, "--",
    )
    violations = []
    for path in names.split("\0"):
        if not is_target(path):
            continue
        patch = git(
            repo, "diff", *diff_options, "--no-color", "--text", "--unified=0",
            "--output-indicator-new=+", "--output-indicator-old=-",
            "--output-indicator-context= ",
            start, head_sha, "--", path,
        )
        violations.extend(added_terms(path, patch))
    return violations


def escape_command(value: str, *, property_value: bool = False) -> str:
    value = value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    if property_value:
        value = value.replace(":", "%3A").replace(",", "%2C")
    return value


def github_annotation(violation: Violation) -> str:
    path = escape_command(violation.path, property_value=True)
    message = escape_command(violation.message)
    return f"::{violation.severity} file={path},line={violation.line}::{message}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Base branch or commit; comparison starts at the merge base")
    parser.add_argument("--head", default="HEAD", help="PR head branch or commit (default: HEAD)")
    parser.add_argument("--github-actions", action="store_true", help="Emit file and line annotations")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parent.parent
    try:
        violations = check(repo, args.base, args.head)
    except RuntimeError as error:
        message = f"Unable to check Simplified Chinese terms: {error}"
        if args.github_actions:
            print(f"::error::{escape_command(message)}")
        else:
            print(message, file=sys.stderr)
        return 2

    for violation in violations:
        if args.github_actions:
            print(github_annotation(violation))
        else:
            print(f"{violation.path}:{violation.line}: {violation.severity}: {violation.message}")
    if violations:
        errors = sum(violation.severity == "error" for violation in violations)
        warnings = len(violations) - errors
        print(f"Found {errors} error(s) and {warnings} warning(s) in added Simplified Chinese lines.")
        return 1 if errors else 0
    print("No terminology issues in added Simplified Chinese lines.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
