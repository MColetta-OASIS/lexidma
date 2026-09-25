#!/usr/bin/env python3
"""Count figure widths in the DocBook source, the Markdown edition and the
published HTML.

    count_figure_widths.py DOCBOOK_DIR MARKDOWN.md PUBLISHED.html > widths.json

DocBook: every contentwidth attribute under DOCBOOK_DIR (*.xml), by value.
Markdown and HTML: every <img> element, and its width attribute by value.
Files are read as bytes and decoded leniently, because the published HTML is
ISO-8859-1.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

IMG = re.compile(rb"<img\b[^>]*>", re.I)
WIDTH = re.compile(rb'\bwidth="([^"]*)"', re.I)
CONTENTWIDTH = re.compile(rb'\bcontentwidth="([^"]*)"')


def ranked(counter: Counter, key: str) -> list[dict]:
    """Most frequent first, so /0 is the dominant value."""
    return [{key: v, "count": n} for v, n in counter.most_common()]


def imgs(path: Path) -> dict:
    tags = IMG.findall(path.read_bytes())
    widths = Counter(m.group(1).decode("latin-1")
                     for t in tags for m in [WIDTH.search(t)] if m)
    return {"file": str(path), "img_elements": len(tags),
            "img_without_width": len(tags) - sum(widths.values()),
            "img_width": ranked(widths, "width")}


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    docbook, md, html = (Path(a) for a in sys.argv[1:])
    cw = Counter()
    for f in sorted(docbook.rglob("*.xml")):
        cw.update(v.decode("latin-1") for v in CONTENTWIDTH.findall(f.read_bytes()))
    json.dump({"docbook": {"dir": str(docbook), "contentwidth": ranked(cw, "value")},
               "markdown": imgs(md), "published_html": imgs(html)},
              sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
