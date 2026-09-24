# DocBook to Markdown Converter

## Purpose

This directory holds the tooling that converts the DMLex DocBook 4.5 source
(`dmlex-v1.0/specification`) into a single OASIS-style Markdown document and
verifies the result against the published HTML of the same stage. The committed
output is in `dmlex-v1.0/markdown/`. It is a starting point for authoring later
versions of DMLex in Markdown, and it reproduces the text of DMLex Version 1.0
OASIS Standard as published at
<https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.html>.

| File | Role |
|---|---|
| `build.sh` | End-to-end driver: resolve XIncludes, regenerate the UML diagram, convert, copy images, verify |
| `docbook2md.py` | Converter from resolved DocBook XML to Markdown |
| `verify_md.py` | Comparison of the Markdown against the published HTML |
| `allow.json` | Accepted deviations between the two, each with a reason |

## Provenance

The tooling and the generated Markdown are provided by OASIS staff (TC
Administration) as a formatting service. The generated Markdown reproduces the
text of the TC's approved DMLex Version 1.0 OASIS Standard without technical
change. The tooling is OASIS staff infrastructure and is not a contribution to
the TC's work product.

## Requirements

- Python 3.8 or later (standard library only)
- `xmllint` (libxml2)
- Graphviz `dot` and `m4`, to regenerate `dmlex_uml.svg` for Appendix D
- pandoc 3.x, for verification only; older releases parse GitHub Flavored
  Markdown differently and produce spurious differences
- `curl`, when the published HTML is given as a URL

On Debian or Ubuntu: `apt-get install libxml2-utils graphviz m4 curl`, plus the
pandoc `.deb` from <https://github.com/jgm/pandoc/releases>. On macOS all of these
are available from Homebrew.

## Usage

```
tools/docbook-to-markdown/build.sh SPEC_DIR OUT_DIR [PUBLISHED_HTML]
```

| Argument | Meaning |
|---|---|
| `SPEC_DIR` | The DocBook source directory, `dmlex-v1.0/specification` |
| `OUT_DIR` | Receives `dmlex-<version>-<stage>.md`, the images it references, and the verification report |
| `PUBLISHED_HTML` | Optional. Path or URL of the published HTML to verify against. Omitted, verification is skipped |

Version and stage are read from `docbook/dbgenent.mod`, so the output name
follows the source. Regenerating the committed edition:

```
tools/docbook-to-markdown/build.sh dmlex-v1.0/specification dmlex-v1.0/markdown \
    https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.html
```

The script exits non-zero if the merge fails, if the converter meets a
reference to an unknown id, or if verification fails. The last line of output
is `RESULT: PASS` or `RESULT: FAIL`.

The GitHub Actions workflow `.github/workflows/docbook-to-markdown.yml` runs the
same command on every change to the specification source or to this tooling,
and fails if the committed `dmlex-v1.0/markdown/dmlex-v1.0-os.md` differs from a
fresh conversion. The fresh output is uploaded as the `dmlex-markdown` artifact.

## Rendering Rules

The converter follows the TC stylesheet
(`stylesheets/oasis-specification-html.xsl`) so that the Markdown reads the same
as the published HTML, and it follows the page layout of the OASIS Markdown
specifications (CSAF, NIEM) for front matter.

- `<glossterm>` is uppercased, which is how the stylesheet renders the BCP 14
  key words.
- A section or appendix with `role="normative"` or `role="informative"` gets a
  ` (Normative)` or ` (Informative)` suffix after its title.
- Every DocBook `id` becomes an HTML anchor (`<a id='...'></a>`), so `olink`,
  `xref` and `link` targets resolve, and existing deep links into the published
  HTML (for example `#core_entry` or `#ex15`) work unchanged against the
  Markdown.
- A cross-reference to a section is rendered as `Section N, "Title"`, and to an
  appendix as `Appendix X, "Title"`, matching DocBook generated text.
- Examples are numbered document-wide in the body (Example 1, 2, ...) and
  separately within each appendix (Example A.1, A.2, ...), as in the published
  HTML.
- Paragraphs placed directly in a section that contains a bibliography are
  omitted, because the TC stylesheet suppresses them in the published output.
- Program listings are fenced code blocks with their content copied byte for
  byte; the fence language is taken from the `xml:base` of the included file
  (`json`, `xml`, `turtle`, `nvh`, `sql`).
- The table of contents lists headings to three levels.
- A `<graphic>` with a `contentwidth` in centimetres becomes an HTML
  `<img width>` in pixels at 90 dpi, which is how the stylesheet sizes it
  (the 16cm figures render 567px wide). Without the width an SVG draws at its
  natural size and the UML diagram runs off the page.

## Verification

`verify_md.py` reduces both documents to visible text (the Markdown through
pandoc, GFM to HTML) and compares them. It checks:

- **Word sequence.** Both texts are tokenised and aligned with `difflib`. Every
  region where they disagree is reported with context. Tables of contents are
  excluded from both sides.
- **Code blocks.** The number of `<pre>` blocks matches, and each block is
  identical to its published counterpart in document order, apart from trailing
  whitespace on each line.
- **Headings.** Every numbered heading in the published HTML appears in the
  Markdown, in the same order.
- **Internal anchors.** Every `#id` link in the Markdown has a matching anchor.
- **Images.** Every image the Markdown references, as a Markdown image or an
  HTML `<img>`, exists on disk under the output directory, and the image count
  matches the published HTML.

`docs.oasis-open.org` is served through Cloudflare, which replaces email
addresses in the page with an encoded placeholder. The verifier decodes these
before comparing, so a live URL and a saved copy give the same result.

`allow.json` lists the deviations accepted between the two documents. Each
entry names the published text, the Markdown text and the reason. They cover
layout differences inherited from the OASIS Markdown template (the Specification
URIs label, the stage labels of Naming Directives v1.7, the position of the key
words paragraph), the HTML page footer, and the source defects below. Any
difference not listed there fails the check. The report is written to
`dmlex-<version>-<stage>-verification.json` next to the Markdown.

## Known Source Defects

These are defects in the DocBook source of the OASIS Standard. The converter
does not correct text; where a defect reaches the published HTML it reaches the
Markdown too, except the first, which is dropped because it is a markup error
rather than content.

1. `ReviewChangeTracking/csd04.xml` and `ReviewChangeTracking/csd03.xml` each
   start their title with an empty `<ulink url="csd04.xml"/>` (or
   `csd03.xml`). The stylesheet prints the URL as link text, so the published
   headings of F.1.2.1 and F.1.2.2 read `csd04.xmlTracking of changes ...` and
   `csd03.xmlTracking of changes ...`. The Markdown drops the empty link and
   `allow.json` records the difference.
2. In the F.1.2 paragraphs of the same two files, the link text of the
   Committee Specification Draft 04 and 03 PDF links ends in `.pdf.pdf`, while
   the link target ends in `.pdf`.
3. The citation format paragraph in `dmlex.xml` reads `OASIS &standard;`, and
   the entity already expands to `OASIS Standard`, so the published citation
   reads "OASIS OASIS Standard".
4. The `Makefile` rule for `dmlex.dot.content` pipes through GNU
   `head -n-1` and runs `nvh2dot.py`, whose first line is `#!/usr/bin/python`.
   Neither is available on a stock macOS system, so `make dmlex_uml.svg`
   fails there. `build.sh` regenerates the diagram with `python3`, `sed` and
   `tail` instead, and leaves the result at `dmlex-v1.0/specification/dmlex_uml.svg`,
   which the repository already ignores.
