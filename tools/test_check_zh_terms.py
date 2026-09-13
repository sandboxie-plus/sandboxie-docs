"""Exercise the terminology check against real, isolated Git histories."""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from check_zh_terms import Violation, check, github_annotation, is_target


class TermCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.env = os.environ.copy()
        self.env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            self.env.pop(name, None)
        env_patch = patch.dict(os.environ, self.env, clear=True)
        env_patch.start()
        self.addCleanup(env_patch.stop)
        self.git("init", "-b", "main")
        for key, value in {
            "user.name": "Checker Test",
            "user.email": "checker@example.invalid",
            "commit.gpgsign": "false",
            "core.hooksPath": str(self.repo / "no-hooks"),
            "core.autocrlf": "false",
        }.items():
            self.git("config", key, value)
        self.write("README.md", "Fixture\n")
        self.base = self.commit()

    def git(self, *args):
        return subprocess.run(
            ["git", "-C", str(self.repo), *args], env=self.env,
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.decode("utf-8").strip()

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="")

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "-m", "Fixture change")
        return self.git("rev-parse", "HEAD")

    def test_scope(self):
        for path in ("docs/zh-CN/README.md", "docs/zh-CN/Content/Test.md", "README_zh-CN.md"):
            with self.subTest(path=path):
                self.assertTrue(is_target(path))
        for path in ("README.md", "docs/Content/Test.md", "docs/zh-TW/Test.md",
                     "docs/zh-CN/Test.png", "other/README_zh-CN.md"):
            with self.subTest(path=path):
                self.assertFalse(is_target(path))

    def test_terms_and_literal_paths(self):
        path = "docs/zh-CN/Content/中文 [one] file.md"
        self.write(path, "沙盒、磁盘和工具箱\n沙箱中的沙箱\n沙盘中的沙盒\n")
        self.write("docs/zh-CN/Content/中文 o file.md", "沙盒\n")
        self.write("docs/Content/English.md", "沙箱\n沙盒管理器\n")
        self.write("docs/zh-TW/Example.md", "沙箱\n沙盤管理器\n沙箱管理器\n")
        self.commit()
        self.assertEqual(check(self.repo, self.base), [
            Violation(path, 2, "沙箱"), Violation(path, 3, "沙盘"),
        ])

    def test_manager_names_receive_context_warning_without_duplicate_terms(self):
        path = "docs/zh-CN/Content/Managers.md"
        terms = ("沙盘管理器", "沙盒管理器", "沙箱管理器")
        self.write(path, "\n".join(terms) + "\n")
        self.commit()
        findings = check(self.repo, self.base)
        self.assertEqual(findings, [
            Violation(path, line, term) for line, term in enumerate(terms, 1)
        ])
        for finding in findings:
            with self.subTest(term=finding.term):
                self.assertEqual(finding.severity, "warning")
                self.assertTrue("SandMan" in finding.message)
                self.assertTrue("Sandboxie Plus" in finding.message)
                self.assertTrue("Sandboxie Control" in finding.message)
                self.assertTrue("Classic" in finding.message)
                self.assertTrue("Exact UI label quotations may be kept" in finding.message)

    def test_manager_names_do_not_hide_standalone_deprecated_terms(self):
        path = "docs/zh-CN/Content/Mixed.md"
        self.write(path, "沙盘管理器、沙箱管理器、沙盘、沙箱\n")
        self.commit()
        findings = check(self.repo, self.base)
        self.assertEqual(findings, [
            Violation(path, 1, term) for term in ("沙盘", "沙盘管理器", "沙箱", "沙箱管理器")
        ])
        self.assertEqual([finding.severity for finding in findings], [
            "error", "warning", "error", "warning",
        ])

    def test_canonical_manager_names_are_accepted(self):
        self.write("docs/zh-CN/Content/Managers.md", "SandMan\nSandboxie Control\n沙盒\n")
        self.commit()
        self.assertEqual(check(self.repo, self.base), [])

    def test_both_readmes_are_checked(self):
        self.write("README_zh-CN.md", "沙箱\n")
        self.write("docs/zh-CN/README.md", "沙盘\n")
        self.commit()
        self.assertEqual(check(self.repo, self.base), [
            Violation("README_zh-CN.md", 1, "沙箱"),
            Violation("docs/zh-CN/README.md", 1, "沙盘"),
        ])

    def test_unchanged_legacy_line_is_ignored_but_edited_line_is_checked(self):
        path = "docs/zh-CN/Content/Example.md"
        self.write(path, "沙箱。\n沙盒管理器\n原有内容\n")
        base = self.commit()
        self.write(path, "沙箱。\n沙盒管理器\n原有内容\n新增沙盒说明\n")
        self.commit()
        self.assertEqual(check(self.repo, base), [])
        self.write(path, "沙箱！\n沙盒管理器\n原有内容\n新增沙盒说明\n")
        self.commit()
        self.assertEqual(check(self.repo, base), [Violation(path, 1, "沙箱")])

    def test_deleted_file_and_removed_line_are_ignored(self):
        removed = "docs/zh-CN/Content/Removed.md"
        kept = "docs/zh-CN/Content/Kept.md"
        self.write(removed, "沙箱\n沙箱管理器\n")
        self.write(kept, "沙盘\n沙盒管理器\n保留内容\n")
        base = self.commit()
        (self.repo / removed).unlink()
        self.write(kept, "保留内容\n")
        self.commit()
        self.assertEqual(check(self.repo, base), [])

    def test_multiple_hunks_plus_prefix_and_missing_final_newline(self):
        path = "docs/zh-CN/Content/Hunks.md"
        lines = [f"原有内容 {i}" for i in range(20)]
        self.write(path, "\n".join(lines))
        base = self.commit()
        lines[1] = "+++沙箱"
        lines[15] = "沙盒"
        lines[19] = "沙盘"
        self.write(path, "\n".join(lines))
        self.commit()
        self.assertEqual(check(self.repo, base), [
            Violation(path, 2, "沙箱"), Violation(path, 20, "沙盘"),
        ])

    def test_diverged_base_uses_merge_base(self):
        path = "docs/zh-CN/Content/Legacy.md"
        self.write(path, "沙箱\n")
        common = self.commit()
        self.write(path, "沙盒\n")
        base = self.commit()
        self.git("checkout", "-b", "feature", common)
        self.write("README.md", "Feature documentation\n")
        head = self.commit()
        self.assertEqual(check(self.repo, base, head), [])

    def test_move_into_chinese_scope_is_checked(self):
        source = "docs/Content/Move.md"
        target = "docs/zh-CN/Content/Move.md"
        self.write(source, "沙箱\n")
        base = self.commit()
        (self.repo / target).parent.mkdir(parents=True)
        (self.repo / source).rename(self.repo / target)
        self.commit()
        self.assertEqual(check(self.repo, base), [Violation(target, 1, "沙箱")])

    def test_invalid_and_option_like_revisions_fail(self):
        for revision in ("nonexistent-revision", "--help", "--output=unexpected-file"):
            with self.subTest(revision=revision):
                with self.assertRaises(RuntimeError):
                    check(self.repo, revision)
                with self.assertRaises(RuntimeError):
                    check(self.repo, self.base, revision)
        self.assertFalse((self.repo / "unexpected-file").exists())

    def test_large_diff_reaches_last_line(self):
        path = "docs/zh-CN/Content/Large.md"
        self.write(path, ("沙盒说明 " + "a" * 100 + "\n") * 1500 + "沙箱\n")
        self.commit()
        self.assertEqual(check(self.repo, self.base), [Violation(path, 1501, "沙箱")])

    def test_github_annotation_escapes_control_characters(self):
        result = github_annotation(Violation("docs/zh-CN/a%,:\r\n::error.md", 7, "沙箱"))
        self.assertEqual(result, "::error file=docs/zh-CN/a%25%2C%3A%0D%0A%3A%3Aerror.md,line=7::"
                         "Use '沙盒' instead of '沙箱' in Simplified Chinese documentation.")
        warning = Violation("docs/zh-CN/a%,:\r\n::warning.md", 8, "沙盒管理器")
        self.assertEqual(github_annotation(warning),
                         "::warning file=docs/zh-CN/a%25%2C%3A%0D%0A%3A%3Awarning.md,line=8::"
                         + warning.message)

    def test_cli_exit_status_and_annotations(self):
        script = self.repo / "tools" / "check_zh_terms.py"
        script.parent.mkdir()
        shutil.copyfile(Path(__file__).with_name("check_zh_terms.py"), script)

        def run(base, annotations):
            return subprocess.run(
                [sys.executable, str(script), "--base", base]
                + (["--github-actions"] if annotations else []),
                env={**self.env, "PYTHONIOENCODING": "utf-8"},
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8",
            )

        path = "docs/zh-CN/Content/Test.md"
        cases = (
            ("SandMan\n", 0, ()),
            ("沙盒管理器\n", 0, (("warning", 1),)),
            ("沙盘\n", 1, (("error", 1),)),
            ("沙箱管理器\n沙箱\n", 1, (("warning", 1), ("error", 2))),
        )
        for content, status, findings in cases:
            self.write(path, content)
            self.commit()
            for annotations in (False, True):
                with self.subTest(content=content, annotations=annotations):
                    result = run(self.base, annotations)
                    self.assertEqual(result.returncode, status, result.stderr)
                    for severity, line in findings:
                        expected = (f"::{severity} file={path},line={line}::" if annotations
                                    else f"{path}:{line}: {severity}:")
                        self.assertTrue(expected in result.stdout, result.stdout)
                    if not annotations:
                        self.assertFalse("::warning" in result.stdout)
                        self.assertFalse("::error" in result.stdout)
        for annotations in (False, True):
            with self.subTest(invalid_revision=True, annotations=annotations):
                result = run("missing-revision", annotations)
                self.assertEqual(result.returncode, 2)
                if annotations:
                    self.assertIn("::error::Unable to check", result.stdout)  # codespell:ignore assertin
                else:
                    self.assertTrue("Unable to check" in result.stderr)


if __name__ == "__main__":
    unittest.main()
