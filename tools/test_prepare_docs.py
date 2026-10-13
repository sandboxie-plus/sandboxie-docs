"""Tests for isolated, publish-compatible documentation preparation."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import tempfile
import unittest

from prepare_docs import main, prepare_docs


class PrepareDocsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.output = self.root / "build"
        self.write("mkdocs.yml", "site_name: Test\n")
        self.write("material/overrides/main.html", "theme")
        self.write("docs/README.md", "English home")
        self.write("docs/Content/translated.md", "English original")
        self.write("docs/Content/missing.md", "English fallback")
        self.write("docs/PlusContent/missing.md", "Plus fallback")
        self.write("docs/zh-CN/Content/translated.md", "中文原文\n")
        self.write("docs/zh-CN/README.md", "中文首页")
        self.write("docs/zh-CN/Media/image.png", "localized image")

    def write(self, relative: str, content: str) -> None:
        target = self.repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def snapshot(self) -> dict[str, bytes]:
        return {str(path.relative_to(self.repo)): path.read_bytes()
                for path in self.repo.rglob("*") if path.is_file()}

    def test_preserves_translations_and_fills_both_page_directories(self) -> None:
        output, fallback_count = prepare_docs(self.repo, self.output)
        self.assertEqual(output, self.output.resolve())
        self.assertEqual(fallback_count, 2)
        for language in ("zh-CN", "zh"):
            base = output / "docs" / language
            self.assertEqual((base / "Content/translated.md").read_text(encoding="utf-8"), "中文原文\n")
            self.assertEqual((base / "Content/missing.md").read_text(encoding="utf-8"), "English fallback")
            self.assertEqual((base / "PlusContent/missing.md").read_text(encoding="utf-8"), "Plus fallback")
            self.assertEqual((base / "README.md").read_text(encoding="utf-8"), "中文首页")
            self.assertEqual((base / "Media/image.png").read_text(encoding="utf-8"), "localized image")
        self.assertEqual((output / "material/overrides/main.html").read_text(encoding="utf-8"), "theme")
        self.assertTrue((output / "mkdocs.yml").is_file())
        self.assertEqual((output / ".prepared-docs").read_text(encoding="utf-8"), "sandboxie-docs-prepared-v1\n")

    def test_source_files_are_unchanged(self) -> None:
        before = self.snapshot()
        prepare_docs(self.repo, self.output)
        self.assertEqual(before, self.snapshot())
        self.assertFalse((self.repo / "docs/zh").exists())

    def test_rebuilds_zh_without_touching_existing_source_zh(self) -> None:
        self.write("docs/zh/obsolete.md", "stale generated page")
        before = self.snapshot()
        prepare_docs(self.repo, self.output)
        self.assertFalse((self.output / "docs/zh/obsolete.md").exists())
        self.assertEqual(before, self.snapshot())

    def test_fallback_only_copies_top_level_markdown(self) -> None:
        self.write("docs/Content/nested/page.md", "nested")
        self.write("docs/Content/asset.png", "asset")
        prepare_docs(self.repo, self.output)
        self.assertFalse((self.output / "docs/zh/Content/nested").exists())
        self.assertFalse((self.output / "docs/zh/Content/asset.png").exists())
        self.assertTrue((self.output / "docs/Content/nested/page.md").is_file())

    def test_existing_directory_is_not_overwritten(self) -> None:
        self.output.mkdir()
        sentinel = self.output / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "already exists"):
            prepare_docs(self.repo, self.output)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")

    def test_existing_empty_directory_is_rejected(self) -> None:
        self.output.mkdir()
        with self.assertRaisesRegex(ValueError, "already exists"):
            prepare_docs(self.repo, self.output)

    def test_existing_file_is_not_overwritten(self) -> None:
        self.output.write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "already exists"):
            prepare_docs(self.repo, self.output)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "keep")

    def test_output_inside_repository_is_rejected(self) -> None:
        for relative in ("build", "docs/build", "material/build"):
            with self.subTest(relative=relative), self.assertRaisesRegex(ValueError, "outside"):
                prepare_docs(self.repo, self.repo / relative)
            self.assertFalse((self.repo / relative).exists())

    def test_repository_and_ancestor_outputs_are_rejected(self) -> None:
        before = self.snapshot()
        for destination in (self.repo, self.root):
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                prepare_docs(self.repo, destination)
        self.assertEqual(before, self.snapshot())

    def test_missing_input_does_not_create_output(self) -> None:
        (self.repo / "mkdocs.yml").unlink()
        with self.assertRaisesRegex(ValueError, "required source file"):
            prepare_docs(self.repo, self.output)
        self.assertFalse(self.output.exists())

    def test_source_symlinks_are_rejected(self) -> None:
        target = self.repo / "docs/Content/link.md"
        try:
            target.symlink_to(self.repo / "docs/Content/translated.md")
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "source links"):
            prepare_docs(self.repo, self.output)
        self.assertFalse(self.output.exists())

    def test_output_through_symlink_into_input_is_rejected(self) -> None:
        alias = self.root / "alias"
        try:
            alias.symlink_to(self.repo / "docs", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "outside"):
            prepare_docs(self.repo, alias / "build")
        self.assertFalse((self.repo / "docs/build").exists())

    def test_source_directory_link_is_rejected_before_traversal(self) -> None:
        target = self.repo / "docs/loop"
        try:
            target.symlink_to(self.repo / "docs", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        with self.assertRaisesRegex(ValueError, "source links"):
            prepare_docs(self.repo, self.output)
        self.assertFalse(self.output.exists())

    def test_cli_reports_input_error(self) -> None:
        self.output.mkdir()
        errors = StringIO()
        with redirect_stderr(errors):
            result = main(["--repo", str(self.repo), "--output", str(self.output)])
        self.assertEqual(result, 2)
        self.assertTrue("output already exists" in errors.getvalue(), errors.getvalue())


if __name__ == "__main__":
    unittest.main()
