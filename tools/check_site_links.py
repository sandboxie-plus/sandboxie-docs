#!/usr/bin/env python3
"""Check local and same-site links inside generated HTML article elements.

This checks files and HTML fragments, not external URLs or navigation links.
Exit status: 0 for success, 1 for broken links, 2 if checking could not finish.
"""

import argparse
from dataclasses import dataclass, field
from html.parser import HTMLParser
import os
from pathlib import Path
import re
import stat
import sys
from urllib.parse import unquote, urlsplit


DEFAULT_SITE_URL = "https://sandboxie-plus.github.io/sandboxie-docs/"


class CheckFailed(RuntimeError):
    """The site could not be checked completely."""


@dataclass(frozen=True)
class Link:
    line: int
    url: str
    kind: str


@dataclass(frozen=True)
class Diagnostic:
    path: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: error: {self.message}"


@dataclass
class Result:
    html_files: int = 0
    article_pages: int = 0
    local_references: int = 0
    external_references: int = 0
    errors: list[Diagnostic] = field(default_factory=list)


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()
        self.links: list[Link] = []
        self.articles = 0
        self.article_depth = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id") is not None:
            self.anchors.add(attributes["id"])
        if tag == "a" and attributes.get("name") is not None:
            self.anchors.add(attributes["name"])
        if tag == "article":
            self.articles += 1
            self.article_depth += 1
        if self.article_depth and tag in ("a", "img"):
            attribute = "href" if tag == "a" else "src"
            if attribute in attributes:
                self.links.append(Link(
                    self.getpos()[0], attributes[attribute] or "", tag,
                ))

    def handle_endtag(self, tag):
        if tag == "article" and self.article_depth:
            self.article_depth -= 1


def decode_url_part(value: str) -> str:
    if re.search(r"%(?![0-9a-fA-F]{2})", value):
        raise ValueError("invalid percent escape")
    value = unquote(value, encoding="utf-8", errors="strict")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError("control character in URL")
    return value


def normalize_base_path(value: str) -> str:
    try:
        url = urlsplit(value)
        path = decode_url_part(url.path)
    except ValueError as error:
        raise CheckFailed(f"Invalid base path: {error}") from error
    if (url.scheme or url.netloc or url.query or url.fragment
            or not path.startswith("/") or "\\" in path
            or any(part in (".", "..") for part in path.split("/"))):
        raise CheckFailed("Base path must be an absolute URL path without query, fragment, or dot segments")
    return path.rstrip("/") + "/"


def origin(url, default_scheme="https"):
    port = url.port
    scheme = url.scheme or default_scheme
    if (scheme == "http" and port == 80) or (scheme == "https" and port == 443):
        port = None
    return url.hostname, port


def site_options(site_url: str, base_path: str | None):
    try:
        url = urlsplit(site_url)
        if (url.scheme not in ("http", "https") or not url.hostname
                or url.username or url.password or url.query or url.fragment):
            raise ValueError("expected an HTTP(S) URL without credentials, query, or fragment")
        host = origin(url)
    except ValueError as error:
        raise CheckFailed(f"Invalid site URL: {error}") from error
    return normalize_base_path(base_path if base_path is not None else url.path or "/"), host, url.scheme


def inside_site(site: Path, path: Path) -> Path:
    """Resolve symlinks before any read; never follow a target out of the site."""
    resolved = path.resolve()
    if not resolved.is_relative_to(site):
        raise ValueError("target escapes the site directory")
    return resolved


def html_files(site: Path) -> list[Path]:
    pending = [site]
    seen: set[Path] = set()
    files: set[Path] = set()
    while pending:
        directory = pending.pop()
        try:
            directory = inside_site(site, directory)
            if directory in seen:
                continue
            seen.add(directory)
            with os.scandir(directory) as entries:
                for entry in entries:
                    path = Path(entry.path)
                    if entry.is_dir():
                        pending.append(path)
                    elif path.suffix.lower() in (".html", ".htm"):
                        files.add(inside_site(site, path))
        except (OSError, ValueError, RuntimeError) as error:
            raise CheckFailed(f"{directory}:1: Unable to scan HTML: {error}") from error
    return sorted(files)


def check_site(site: Path, base_path: str | None = None, site_url: str = DEFAULT_SITE_URL) -> Result:
    base_path, site_origin, site_scheme = site_options(site_url, base_path)
    try:
        site = site.resolve(strict=True)
        mode = site.stat().st_mode
    except (OSError, ValueError, RuntimeError) as error:
        raise CheckFailed(f"{site}:1: Unable to open site: {error}") from error
    if not stat.S_ISDIR(mode):
        raise CheckFailed(f"{site}:1: Site is not a directory")

    files = html_files(site)
    if not files:
        raise CheckFailed(f"{site}:1: Site contains no HTML files")
    cache: dict[Path, Document] = {}

    def document(path: Path) -> Document:
        if path not in cache:
            try:
                # Paths reaching this function have already passed inside_site.
                content = path.read_text(encoding="utf-8-sig")
                parsed = Document()
                parsed.feed(content)
                parsed.close()
                cache[path] = parsed
            except (OSError, ValueError) as error:
                raise CheckFailed(f"{path.relative_to(site)}:1: Unable to read HTML: {error}") from error
        return cache[path]

    result = Result(html_files=len(files))
    for source in files:
        page = document(source)
        if page.articles:
            result.article_pages += 1
        for link in page.links:
            location = source.relative_to(site).as_posix()

            def problem(message):
                result.errors.append(Diagnostic(location, link.line, f"{link.url!r}: {message}"))

            # Browsers trim whitespace around URL attributes; internal controls
            # are rejected so urlsplit cannot silently remove them.
            raw = link.url.strip(" \t\r\n\f")
            try:
                if any(ord(char) < 32 or ord(char) == 127 for char in raw):
                    raise ValueError("control character in URL")
                url = urlsplit(raw)
                if url.scheme or url.netloc:
                    if (url.scheme not in ("", "http", "https")
                            or origin(url, site_scheme) != site_origin):
                        result.external_references += 1
                        continue
                    path = decode_url_part(url.path).replace("\\", "/")
                    if not (path.startswith(base_path) or path == base_path.rstrip("/")):
                        result.external_references += 1
                        continue
                else:
                    path = decode_url_part(url.path).replace("\\", "/")
                    # Root-relative URLs resolve at the host root, not at a
                    # project site's prefix. Treat other host paths just like
                    # same-host absolute URLs outside this site.
                    if path.startswith("/") and not (
                            path.startswith(base_path) or path == base_path.rstrip("/")):
                        result.external_references += 1
                        continue
                result.local_references += 1
                if not raw and link.kind == "img":
                    raise ValueError("empty image source")
                fragment = decode_url_part(url.fragment)
                if not path:
                    target = source
                elif path.startswith("/"):
                    if path == base_path.rstrip("/"):
                        path = ""
                    elif path.startswith(base_path):
                        path = path[len(base_path):]
                    target = site / path.lstrip("/")
                else:
                    target = source.parent / path
                target = inside_site(site, target)
                if target.is_dir():
                    target = inside_site(site, target / "index.html")
            except (ValueError, RuntimeError) as error:
                problem(str(error))
                continue
            except OSError as error:
                raise CheckFailed(f"{location}:{link.line}: Unable to resolve {link.url!r}: {error}") from error

            try:
                mode = target.stat().st_mode
            except FileNotFoundError:
                problem(f"missing file {target.relative_to(site).as_posix()}")
                continue
            except OSError as error:
                raise CheckFailed(f"{location}:{link.line}: Unable to inspect {link.url!r}: {error}") from error
            if not stat.S_ISREG(mode):
                problem("target is not a regular file")
            elif fragment and target.suffix.lower() in (".html", ".htm"):
                # HTML also defines the legacy #top fragment as the top of the page.
                if fragment not in document(target).anchors and fragment.lower() != "top":
                    problem(f"missing HTML fragment #{fragment} in {target.relative_to(site).as_posix()}")

    if not result.article_pages:
        raise CheckFailed(f"{site}:1: No HTML article elements found; body links were not checked")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, required=True, help="Generated HTML site directory")
    parser.add_argument("--site-url", default=DEFAULT_SITE_URL, help="Published site URL; matching HTTP/HTTPS links are checked locally")
    parser.add_argument("--base-path", help="Override the site URL path prefix (default: path from --site-url)")
    args = parser.parse_args(argv)
    try:
        result = check_site(args.site, args.base_path, args.site_url)
    except CheckFailed as error:
        print(f"Unable to complete article link check: {error}", file=sys.stderr)
        return 2
    for error in result.errors:
        print(error)
    print(
        f"Checked {result.local_references} local/same-site references in article elements on "
        f"{result.article_pages} of {result.html_files} HTML pages; "
        f"{len(result.errors)} error(s). Skipped {result.external_references} external "
        "references; external URLs and navigation links were not checked."
    )
    return 1 if result.errors else 0


if __name__ == "__main__":
    sys.exit(main())
