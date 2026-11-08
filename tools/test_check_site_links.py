"""Check generated-site behavior with small real HTML/file trees."""

from contextlib import redirect_stderr, redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from check_site_links import CheckFailed, check_site, main


class SiteLinkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.site = self.root / "site"
        self.site.mkdir()

    def write(self, path, content):
        target = self.site / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="")
        return target

    def run_cli(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = main(["--site", str(self.site), *args])
        return result, stdout.getvalue(), stderr.getvalue()

    def test_directory_and_flat_urls_relative_and_absolute(self):
        self.write("index.html", '<article><h1 id="home">Home</h1></article>')
        self.write("guide/index.html", '<article><h1 id="part">Guide</h1></article>')
        self.write("flat.html", '<article><h1 id="part">Flat</h1></article>')
        self.write("nested/page.html", '''<article>
<a href="../guide/#part">Directory</a>
<a href="../flat.html#part">Flat</a>
<a href="/sandboxie-docs/guide/#part">Prefixed</a>
<a href="/sandboxie-docs/flat.html#part">Root-relative</a>
<a href="/sandboxie-docs#home">Site root</a>
<a href="../#home">Parent directory</a>
</article>''')
        result = check_site(self.site)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.local_references, 6)

    def test_unicode_encoded_spaces_query_and_legacy_ids(self):
        self.write("one space.html", '<article><h2 id="中文">Title</h2><a name="123"></a><i id="a&amp;b"></i></article>')
        self.write("index.html", '''<article>
<a href="one%20space.html?anything=%ZZ#%E4%B8%AD%E6%96%87">Unicode</a>
<a href="one%20space.html#123">Legacy numeric name</a>
<a href="one space.html#a%26b">HTML entity ID</a>
<a href="#007">Numeric ID</a><i id="007"></i>
</article>''')
        self.assertEqual(check_site(self.site).errors, [])

    def test_same_page_empty_href_and_top(self):
        self.write("index.html", '''<article id="article">
<a href="">Same page</a><a href="#">Top</a><a href="#TOP">Legacy top</a>
<a href="?query#article">Query and fragment</a>
<a href=" #article ">Trimmed</a><a>Not a link</a>
</article>''')
        result = check_site(self.site)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.local_references, 5)

    def test_images_assets_and_svg_fragments(self):
        self.write("images/image space.svg", '<svg xmlns="http://www.w3.org/2000/svg"></svg>')
        self.write("download.zip", 'not parsed as HTML')
        self.write("index.html", '''<article>
<img src="images/image%20space.svg#view" />
<a href="download.zip?dl=1">Download</a>
<img src="missing.png"><img src=""><img>
</article>''')
        result = check_site(self.site)
        self.assertEqual(len(result.errors), 2)
        self.assertTrue("missing file missing.png" in result.errors[0].message)
        self.assertTrue("empty image source" in result.errors[1].message)

    def test_only_article_links_are_checked_and_external_links_are_skipped(self):
        self.write("index.html", '''<nav><a href="missing.html">Navigation</a></nav>
<article><a href="https://example.invalid/no">Web</a>
<a href="//example.invalid/no">Protocol relative</a><a href="mailto:a@example.invalid">Mail</a>
<img src="data:image/png;base64,abc"><a href="sbie://docs/topic">Application</a></article>
<footer><img src="missing-footer.png"></footer>''')
        result = check_site(self.site)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.local_references, 0)
        self.assertEqual(result.external_references, 5)
        code, stdout, stderr = self.run_cli()
        self.assertEqual(code, 0)
        self.assertTrue("navigation links were not checked" in stdout)
        self.assertEqual(stderr, "")

    def test_multiple_articles_and_nested_tags_preserve_line_numbers(self):
        self.write("index.html", '''<article><div>
<a href="missing.html">Missing</a></div></article>
<a href="not-checked.html">Outside</a>
<article><article><span>Nested</span></article>
<a href="#missing">Still inside outer article</a></article>''')
        result = check_site(self.site)
        self.assertEqual([d.line for d in result.errors], [2, 5])
        self.assertTrue(str(result.errors[0]).startswith("index.html:2: error:"))

    def test_repeated_references_report_each_occurrence_but_cache_target(self):
        source = self.write("index.html", '''<article>
<a href="target.html#absent">First</a>
<a href="target.html#absent">Second</a>
<a href="target.html#exists">Valid</a></article>''')
        target = self.write("target.html", '<article id="exists">Target</article>')
        original = Path.read_text
        reads = []

        def read(path, *args, **kwargs):
            reads.append(path)
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", read):
            result = check_site(self.site)
        self.assertEqual([d.line for d in result.errors], [2, 3])
        self.assertEqual(reads.count(source.resolve()), 1)
        self.assertEqual(reads.count(target.resolve()), 1)

    def test_escape_paths_never_read_outside_site(self):
        private = self.root / "private.html"
        private.write_text('<article id="secret">Private</article>', encoding="utf-8")
        self.write("index.html", '''<article>
<a href="../private.html#secret">Outside</a>
<a href="%2e%2e/private.html#secret">Encoded</a>
<a href="..%5cprivate.html#secret">Windows separator</a>
<a href="/sandboxie-docs/../private.html#secret">Prefix escape</a>
</article>''')
        original = Path.read_text

        def read(path, *args, **kwargs):
            self.assertNotEqual(path.resolve(), private.resolve())
            return original(path, *args, **kwargs)

        with patch.object(Path, "read_text", read):
            result = check_site(self.site)
        self.assertEqual(len(result.errors), 4)
        self.assertTrue(all("escapes the site" in d.message for d in result.errors))

    def test_symlink_target_outside_site_is_not_read(self):
        private = self.root / "private.html"
        private.write_text('private contents', encoding="utf-8")
        try:
            (self.site / "external.txt").symlink_to(private)
        except OSError as error:
            self.skipTest(f"Symlink creation unavailable: {error}")
        self.write("index.html", '<article><a href="external.txt">Outside</a></article>')
        result = check_site(self.site)
        self.assertEqual(len(result.errors), 1)
        self.assertTrue("escapes the site" in result.errors[0].message)

    def test_scanning_symlink_directory_outside_site_fails_without_reading(self):
        private = self.root / "private"
        private.mkdir()
        (private / "secret.html").write_text('private contents', encoding="utf-8")
        try:
            (self.site / "outside").symlink_to(private, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"Symlink creation unavailable: {error}")
        self.write("index.html", '<article>Body</article>')
        with patch.object(Path, "read_text", side_effect=AssertionError("No HTML should be read before scanning finishes")):
            code, _, stderr = self.run_cli()
        self.assertEqual(code, 2)
        self.assertTrue("escapes the site" in stderr)

    def test_malformed_local_urls_fail_closed(self):
        self.write("index.html", '''<article>
<a href="bad%ZZ.html">Invalid escape</a><a href="#%FF">Invalid UTF-8</a>
<a href="bad%00.html">NUL</a><a href="bad&#10;name.html">Control</a>
</article>''')
        result = check_site(self.site)
        self.assertEqual(len(result.errors), 4)
        self.assertEqual(self.run_cli()[0], 1)

    def test_custom_base_path_and_prefix_boundary(self):
        self.write("index.html", '<article id="home"><a href="/custom/#home">Home</a></article>')
        self.assertEqual(check_site(self.site, "/custom").errors, [])
        self.write("extra.html", '<article><a href="/custom-other/index.html#home">Wrong prefix</a></article>')
        result = check_site(self.site, "/custom")
        self.assertEqual(result.errors, [])
        self.assertEqual(result.external_references, 1)

    def test_root_relative_paths_follow_the_published_site_prefix(self):
        self.write("topic.html", '<article id="section">Topic</article>')
        self.write("index.html", '''<article>
<a href="/topic.html#missing">Outside project site</a>
<a href="https://sandboxie-plus.github.io/topic.html#missing">Same destination</a>
</article>''')
        result = check_site(self.site)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.external_references, 2)
        self.write("index.html", '<article><a href="/topic.html#section">Root-hosted site</a></article>')
        result = check_site(self.site, site_url="https://sandboxie-plus.github.io/")
        self.assertEqual(result.errors, [])
        self.assertEqual(result.local_references, 1)

    def test_same_site_absolute_urls_use_local_files_for_http_and_https(self):
        self.write("one space.html", '<article id="中文">Body</article>')
        self.write("index.html", '''<article>
<a href="https://sandboxie-plus.github.io/sandboxie-docs/one%20space.html#%E4%B8%AD%E6%96%87">HTTPS</a>
<a href="http://sandboxie-plus.github.io/sandboxie-docs/one%20space.html#中文">HTTP</a>
<a href="//sandboxie-plus.github.io/sandboxie-docs/one%20space.html#中文">Protocol relative</a>
<a href="https://sandboxie-plus.github.io:443/sandboxie-docs/missing.html">Missing file</a>
<a href="http://sandboxie-plus.github.io:80/sandboxie-docs/one%20space.html#missing">Missing fragment</a>
</article>''')
        result = check_site(self.site)
        self.assertEqual(result.local_references, 5)
        self.assertEqual(len(result.errors), 2)
        self.assertEqual(result.external_references, 0)

    def test_same_site_prefix_boundary_and_other_host_or_port_are_external(self):
        self.write("index.html", '''<article>
<a href="https://sandboxie-plus.github.io/sandboxie-docs-other/missing.html">Other prefix</a>
<a href="https://sandboxie-plus.github.io/elsewhere/missing.html">Other site</a>
<a href="https://sandboxie-plus.github.io.example.invalid/sandboxie-docs/missing.html">Other host</a>
<a href="https://sandboxie-plus.github.io:8443/sandboxie-docs/missing.html">Other port</a>
</article>''')
        result = check_site(self.site)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.external_references, 4)

    def test_absolute_same_site_encoded_escape_is_rejected(self):
        self.write("index.html", '''<article>
<a href="https://sandboxie-plus.github.io/sandboxie-docs/%2e%2e/private.html">Escape</a>
<a href="http://sandboxie-plus.github.io/sandboxie-docs%2F..%2Fprivate.html">Encoded separators</a>
</article>''')
        result = check_site(self.site)
        self.assertEqual(len(result.errors), 2)
        self.assertTrue(all("escapes the site" in d.message for d in result.errors))

    def test_site_url_supplies_base_path(self):
        self.write("index.html", '<article id="home"><a href="http://docs.example.invalid/custom/#home">Home</a></article>')
        result = check_site(self.site, site_url="https://docs.example.invalid/custom/")
        self.assertEqual(result.errors, [])
        self.assertEqual(result.local_references, 1)
        self.assertEqual(self.run_cli("--site-url", "https://docs.example.invalid/custom/")[0], 0)

    def test_invalid_site_url_fails(self):
        self.write("index.html", '<article>Body</article>')
        for value in ("relative", "file:///local/", "https://user:password@example.invalid/", "https://example.invalid:bad/", "https://example.invalid/?query"):
            with self.subTest(value=value):
                self.assertEqual(self.run_cli("--site-url", value)[0], 2)

    def test_missing_empty_or_file_site_and_no_articles_fail(self):
        with self.assertRaises(CheckFailed):
            check_site(self.site / "missing")
        self.assertEqual(self.run_cli()[0], 2)
        page = self.write("index.html", '<nav><a href="missing">Not an article</a></nav>')
        with self.assertRaises(CheckFailed):
            check_site(page)
        code, _, stderr = self.run_cli()
        self.assertEqual(code, 2)
        self.assertTrue("No HTML article elements" in stderr)

    def test_invalid_base_path_fails(self):
        self.write("index.html", '<article>Body</article>')
        for value in ("relative", "https://example.invalid/site/", "/../site/", "/site/?query", "/bad%FF/"):
            with self.subTest(value=value):
                self.assertEqual(self.run_cli("--base-path", value)[0], 2)

    def test_unreadable_or_non_utf8_html_is_execution_failure(self):
        page = self.write("index.html", '<article>Body</article>')
        with patch.object(Path, "read_text", side_effect=PermissionError("denied")):
            code, _, stderr = self.run_cli()
        self.assertEqual(code, 2)
        self.assertTrue("Unable to read HTML" in stderr)
        page.write_bytes(b'\xff\xfeinvalid')
        self.assertEqual(self.run_cli()[0], 2)

    def test_scan_failure_is_not_a_clean_result(self):
        self.write("index.html", '<article>Body</article>')
        with patch("check_site_links.os.scandir", side_effect=PermissionError("denied")):
            code, _, stderr = self.run_cli()
        self.assertEqual(code, 2)
        self.assertTrue("Unable to scan HTML" in stderr)

    def test_unresolvable_site_is_execution_failure(self):
        with patch.object(Path, "resolve", side_effect=RuntimeError("Symlink loop")):
            code, _, stderr = self.run_cli()
        self.assertEqual(code, 2)
        self.assertTrue("Unable to open site" in stderr)

    def test_cli_broken_link_exit_and_diagnostic(self):
        self.write("index.html", '<article>\n<a href="missing.html">Missing</a>\n</article>')
        code, stdout, stderr = self.run_cli()
        self.assertEqual(code, 1)
        self.assertTrue("index.html:2: error:" in stdout)
        self.assertTrue("1 error(s)" in stdout)
        self.assertEqual(stderr, "")


if __name__ == "__main__":
    unittest.main()
