from bs4 import BeautifulSoup
from . import core
import bs4
import re


__all__ = ["to_html"]


def to_html(path: str, indent: int = 4, engine: core.Engine = core.BaseEngine):
    doc = engine.convert(open(path).read())

    html = f"<!DOCTYPE html><html>" \
           f"<head><meta name='viewport' content='width=device-width, initial-scale=1'>" \
           f"<body>{doc}</body></html>"

    return BeautifulSoup(html, 'html.parser').prettify(indent_width=indent)  # type:ignore


def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))


r = re.compile(r'^(\s*)', re.MULTILINE)
orig_prettify = bs4.BeautifulSoup.prettify
bs4.BeautifulSoup.prettify = prettify
