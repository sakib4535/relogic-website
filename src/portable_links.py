"""Keep static page links usable from disk, a subdirectory, or a web host."""
from __future__ import annotations

import html
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit


def file_href(root: Path, page: Path, value: str) -> str:
    """Resolve a local site link and emit a path relative to its HTML file."""
    if not value or value.startswith(('#', '//')):
        return value
    parts = urlsplit(value)
    if parts.scheme or parts.netloc:
        return value
    page_dir = page.parent.as_posix()
    path = parts.path
    if not path:
        path = page.as_posix()
    elif path.startswith('/'):
        path = path.lstrip('/')
    else:
        path = posixpath.normpath(posixpath.join(page_dir, path))
    path = path or 'index.html'
    target = root / unquote(path)
    if target.is_dir():
        path = path.rstrip('/') + '/index.html'
    elif not target.is_file() and (root / (unquote(path) + '.html')).is_file():
        path += '.html'
    relative = posixpath.relpath(path, page_dir or '.')
    return urlunsplit(('', '', relative, parts.query, parts.fragment))


class _RelativeHTML(HTMLParser):
    def __init__(self, root: Path, page: Path, document: str):
        super().__init__(convert_charrefs=False)
        self.root, self.page, self.document = root, page, document
        self.offsets = [0] + [match.end() for match in re.finditer('\n', document)]
        self.edits = []
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        original = self.get_starttag_text()
        def repair(match):
            value = html.unescape(match['value'])
            fixed = file_href(self.root, self.page, value)
            if fixed == value:
                return match[0]
            return match['prefix'] + match['quote'] + html.escape(fixed, quote=True) + match['quote']
        updated = re.sub(
            r'(?P<prefix>\s(?:href|src|poster|action|data-src)\s*=\s*)(?P<quote>[\'\"])(?P<value>.*?)(?P=quote)',
            repair, original, flags=re.I | re.S)
        if original != updated:
            line, col = self.getpos()
            offset = self.offsets[line - 1] + col
            self.edits.append((offset, offset + len(original), updated))

    handle_startendtag = handle_starttag

    def result(self):
        text = self.document
        for start, end, replacement in reversed(self.edits):
            text = text[:start] + replacement + text[end:]
        return text


def portable_html(root: Path, page: Path, document: str) -> str:
    return _RelativeHTML(root, page, document).result()
