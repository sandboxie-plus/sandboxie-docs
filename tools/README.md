# Simplified Chinese terminology check

Use **沙盒** for Sandboxie containers in Simplified Chinese. The community
[poll](https://github.com/sandboxie-plus/Sandboxie/discussions/5546) and
[terminology update](https://github.com/sandboxie-plus/Sandboxie/pull/5582)
established this convention; [documentation issue #250](https://github.com/sandboxie-plus/sandboxie-docs/issues/250)
tracks its adoption here.

The pull request check flags `沙箱` and `沙盘` in added lines of
`docs/zh-CN/**/*.md` (including `docs/zh-CN/README.md`) and the root
`README_zh-CN.md`. It matches the complete terms, so words such as `磁盘` and
`工具箱` are allowed. Other languages are outside its scope.

The phrases `沙盘管理器`, `沙盒管理器` and `沙箱管理器` produce warnings for
manual review. Use `SandMan` for the Plus UI and `Sandboxie Control` for the
Classic UI; exact quotations of translated UI labels may be kept. These warnings
do not fail the check. A manager phrase receives one warning, without a second
error for the `沙盘` or `沙箱` within it. Separate uses of those deprecated terms
on the same line still produce errors.

The comparison uses the merge base of the base and head commits. Existing
lines are left alone until edited; changing even one character checks the
whole new line. Deleted lines are ignored. Renames are treated as a deletion
and an addition, so the contents of a file moved into a checked path are checked.
The rule also applies to code blocks and quotations on changed lines.
Review each reported use in context: containers are `沙盒`, while product
names such as `Sandboxie` remain untranslated. The checker does not edit files.

Run locally with Python 3.10 or later and Git; no Python packages are needed:

```sh
python tools/check_zh_terms.py --base origin/main
python -m unittest discover -s tools -p 'test_check_zh_terms.py'
```

Only committed changes are checked. Use `--head <commit>` to check a different
commit, and ensure both revisions and their common history are available locally.
Exit codes are 0 for success (including warnings only), 1 for deprecated term
errors and 2 for a check that could not be completed. CI uses `--github-actions`
to report the affected files and lines.
