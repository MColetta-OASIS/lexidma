# DMLex Publication Assurance, 27 September 2026

This record checks the Markdown edition of DMLex Version 1.0 OASIS Standard
against both published originals: the HTML and the PDF. It was made with
[OASIS-Docs/publication-assurance v1.10.0](https://github.com/OASIS-Docs/publication-assurance/releases/tag/v1.10.0)
from a clean checkout of that release. It replaces the text comparison in
[the 24 September record](../2026-09-24/), which could not see list letters
or a PDF's page numbers.

## What was wrong, and is fixed

Comparing the PDFs found three faults that every earlier check had passed:

1. **Section 2's lists were numbered 1., 2., 3.** where the standard letters
   them a., b., c. (and i., ii. below that). The words were identical, but
   the text says "as per point c. above", so the letters carry meaning.
2. **The table of contents was missing 38 entries**: A.2.2.1 to A.2.2.34 and
   F.1.2.1 to F.1.2.4, which the published contents list.
3. **The rendered PDF's contents had no page numbers.**

All three are fixed in the v1.0 edition and in
[v1.1 WD01](../../../../dmlex-v1.1/dmlex-v1.1-wd01.md).

## Results

| Check | Result |
|---|---|
| Markdown and its HTML against the published HTML ([report](verification/verify-md-rendered.txt)) | PASS. 61,260 tokens in order with 0 unexplained differences, 311 headings, all 316 code blocks identical, 1,133 list items, every list numbered as published, all 171 contents entries |
| Rendered PDF against the published PDF ([report](verification/verify-pdf.txt)) | PASS. 65,790 tokens, 0 unexplained differences, all 171 contents entries numbered, the footer on all 195 pages |
| The 24 September PDF, the same check ([report](verification/verify-pdf-24sep.txt)) | FAIL. 0 of its contents entries numbered |
| Page review ([grade](page-review/grade-sonnet.txt)) | ACCEPTED. 36 page pairs, including one with a planted fault |
| Gate, v1.1 WD01 | 5 blockers, all from the three questions below |

The PDF comparison accepts 42 differences, each with its reason in
[the profile](https://github.com/OASIS-Docs/publication-assurance/blob/v1.10.0/converters/docbook-to-markdown/profiles/dmlex/allow-pdf.json).
Most are the OASIS Markdown template's (for example "This stage" where the
original says "This version"). The rest are faults in the published PDF
itself, which the Markdown edition does not share:
- its font has no `ň` or `ō`, so `sklizeň` and `skulō` print as `sklize#` and
  `skul#` (15 places);
- where a page break splits Examples A.63, A.64, A.87 and A.88, the caption
  prints on a line of the example's code.

## The page review

A reviewer compared 36 pairs of pages, published on the left and rendered on
the right. One pair had the page numbers erased from a contents page, and the
reviewer was not told. The review counts only when the lines it copies from
each page are on that page, and when it names the erased numbers.

- Sonnet named the erased numbers and the `csd04.xml` heading defect below.
  It was accepted after re-running 5 pairs where it had copied the wrong page
  or too little. [Pair 020](page-review/pair-020.png) is the planted fault.
- Haiku copied lines that are not on the page for 21 of the 36 pairs, and
  missed the planted fault ([grade](page-review/grade-haiku.txt)). It was
  rejected.

Of the differences Sonnet reported, all were template styling or published
defects except one worth knowing: the diagrams print about 6% smaller than in
the published PDF (15 cm against 16 cm), with the same content, still legible
([pair 034](page-review/pair-034.png)).

## Still for the TC to decide

These are in the published v1.0 and carry into v1.1 until the TC changes
them:

1. Both JSON schemas declare the same `$id`, and it serves a web page, not a
   schema.
2. Appendix C cites `dmlex.nvh`, which is not in the repository.
3. The [XML Catalogs] reference points at a member-only URL.

The published F.1.2.1 and F.1.2.2 headings also begin with a stray
`csd04.xml` and `csd03.xml`; the Markdown edition drops them.

## Files

- [rendered/](rendered/): the v1.0 OS and v1.1 WD01 PDFs from this release
- [verification/](verification/): the verifiers' full reports, text and JSON
- [page-review/](page-review/): the brief, every review, both grades, the key
