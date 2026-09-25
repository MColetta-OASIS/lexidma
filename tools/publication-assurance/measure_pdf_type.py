#!/usr/bin/env python3
"""Measure the type in one or more PDFs from their text layer.

    measure_pdf_type.py LABEL=FILE.pdf [LABEL=FILE.pdf ...] > type.json

For each PDF: the page count, every (font, size) pair weighted by the number
of characters set in it, and three roles read off that table:

  body    the most-used font that is not a monospace face
  code    the most-used monospace face (Courier, Mono, Consolas)
  footer  the most-used size among spans in the bottom 50pt of the page, and
          the number of pages with any text in that band

and the horizontal extent of the text column (min x0, max x1 of every span
outside the footer band), in points.

Sizes are rounded to 0.1pt. Shares are percentages, to one decimal, of the
non-space characters outside the footer band. A subset prefix (ABCDEF+) is dropped from font names. Needs
PyMuPDF.
"""
import json
import re
import sys
from collections import Counter

import fitz

MONO = re.compile(r"courier|mono|consolas", re.I)
FOOTER_BAND = 50.0


def measure(path: str) -> dict:
    doc = fitz.open(path)
    chars = Counter()
    footer = Counter()
    footer_pages = 0
    x0 = x1 = None
    for page in doc:
        bottom = page.rect.height - FOOTER_BAND
        has_footer = False
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    n = len(span["text"].strip())
                    if not n:
                        continue
                    font = span["font"].split("+", 1)[-1]
                    size = round(span["size"], 1)
                    if span["bbox"][1] >= bottom:
                        footer[size] += n
                        has_footer = True
                        continue
                    chars[(font, size)] += n
                    x0 = span["bbox"][0] if x0 is None else min(x0, span["bbox"][0])
                    x1 = span["bbox"][2] if x1 is None else max(x1, span["bbox"][2])
        footer_pages += has_footer
    total = sum(chars.values())

    def role(pred):
        for (font, size), n in chars.most_common():
            if pred(font):
                return {"font": font, "size": size, "share_pct": round(100 * n / total, 1)}
        return None

    return {
        "file": path,
        "pages": doc.page_count,
        "characters": total,
        "body": role(lambda f: not MONO.search(f)),
        "code": role(lambda f: bool(MONO.search(f))),
        "footer": ({"size": footer.most_common(1)[0][0], "pages": footer_pages}
                   if footer else None),
        "text_column_pt": {"x_min": round(x0, 1), "x_max": round(x1, 1)},
        "fonts": [{"font": f, "size": s, "characters": n,
                   "share_pct": round(100 * n / total, 1)}
                  for (f, s), n in chars.most_common(12)],
    }


def main() -> int:
    if len(sys.argv) < 2 or any("=" not in a for a in sys.argv[1:]):
        print(__doc__, file=sys.stderr)
        return 2
    out = {}
    for arg in sys.argv[1:]:
        label, path = arg.split("=", 1)
        out[label] = measure(path)
    json.dump(out, sys.stdout, indent=1)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
