# DocBook to Markdown

## Purpose

The Markdown edition of DMLex Version 1.0 OASIS Standard in
`dmlex-v1.0/markdown/` is generated from the DocBook source in
`dmlex-v1.0/specification` and checked against the published standard at
<https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.html>. It is a
starting point for writing later versions of DMLex in Markdown.

The converter and the verifier are part of the OASIS publication tooling,
[OASIS-Docs/publication-assurance](https://github.com/OASIS-Docs/publication-assurance),
and this repository uses them from a pinned release (v1.9.1). DMLex is that
converter's first profile: what is particular to DMLex (its main file, its
entities, the UML figure its build generates, and the accepted differences
from the published HTML with their reasons) lives in
[`converters/docbook-to-markdown/profiles/dmlex/`](https://github.com/OASIS-Docs/publication-assurance/tree/v1.9.1/converters/docbook-to-markdown/profiles/dmlex).
The walkthrough, with every command, is
[docs/CONVERTING.md](https://github.com/OASIS-Docs/publication-assurance/blob/v1.9.1/docs/CONVERTING.md).

## Provenance

The tooling and the generated Markdown are provided by OASIS staff (TC
Administration) as a formatting service. The Markdown reproduces the text of
the TC's approved DMLex Version 1.0 OASIS Standard without technical change.
The tooling is OASIS staff infrastructure, not a contribution to the TC's
work product.

## Regenerating the edition

```bash
git clone --depth 1 --branch v1.9.1 https://github.com/OASIS-Docs/publication-assurance _pa
_pa/converters/docbook-to-markdown/build.sh --profile dmlex dmlex-v1.0/specification out \
    https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.html
diff out/dmlex-v1.0-os.md dmlex-v1.0/markdown/dmlex-v1.0-os.md
```

Requirements: Python 3.10 or later, `xmllint` (libxml2), Graphviz `dot` and
`m4` (for the UML figure), and pandoc 3.x for the verification. The last line
printed is `RESULT: PASS` or `RESULT: FAIL`.

The workflow `.github/workflows/docbook-to-markdown.yml` runs the same
conversion on every change to the specification source or the edition. It
fails if the verification fails against the snapshot of the published page
that the release carries, or if the committed Markdown differs from a fresh
conversion. It also checks the live page, reporting without blocking, so a
Cloudflare challenge or an outage cannot fail the build.

## What the verification proves

Against the published OASIS Standard, the edition has:

- every word in the same order (61,260 tokens), with 10 accepted differences,
  each with its reason in the profile;
- all 311 numbered headings, in order;
- all 316 code blocks byte for byte;
- the same 1,133 list items, 50 images in the same order, and the same 93
  external link targets.

## Known source defects

These are in the DocBook source of the OASIS Standard. The converter does not
correct text; where a defect reaches the published HTML it reaches the
Markdown too, except the first, which is a markup error, not content.

1. `ReviewChangeTracking/csd04.xml` and `csd03.xml` each start their title
   with an empty `<ulink url="csd04.xml"/>` (or `csd03.xml`), so the published
   headings of F.1.2.1 and F.1.2.2 read `csd04.xmlTracking of changes ...`.
2. In the same two files the link text of the CSD04 and CSD03 PDF links ends
   in `.pdf.pdf`, while the link target ends in `.pdf`.
3. The citation format in `dmlex.xml` reads `OASIS &standard;`, and the entity
   already expands to `OASIS Standard`, so the citation reads "OASIS OASIS
   Standard".
4. The `Makefile` builds `dmlex_uml.svg` with GNU `head -n-1` and
   `#!/usr/bin/python`, neither available on a stock macOS. The DMLex profile
   rebuilds the figure with `python3`, `sed` and `tail`.
5. `nvh2dot.py` walks a Python set, so the diagram's layout changes from run
   to run; the profile fixes the hash seed, and the nodes and edges match the
   published `dmlex_uml.svg`.
