# DMLex Publication Assurance, 24 September 2026

[![Text match](https://img.shields.io/badge/text_vs_published-0_differences-2f9e44)](dmlex-rendering-comparison-2026-09-24.pdf)
[![Code blocks](https://img.shields.io/badge/code_blocks-316%2F316_identical-2f9e44)](dmlex-rendering-comparison-2026-09-24.pdf)
[![Audit](https://img.shields.io/badge/publication_audit-PASS-2f9e44)](dmlex-markdown-edition-publication-audit-2026-09-24.pdf)
[![WD01 gate](https://img.shields.io/badge/v1.1_WD01_gate-3_TC_decisions-f08c00)](#what-the-tc-needs-to-decide)
[![pub-check](https://img.shields.io/badge/oasis--pub--check-v1.4.2-2c4a8a)](https://github.com/OASIS-Docs/publication-assurance/releases/tag/v1.4.2)
[![DocBook to Markdown](https://github.com/MColetta-OASIS/lexidma/actions/workflows/docbook-to-markdown.yml/badge.svg?branch=markdown-conversion)](https://github.com/MColetta-OASIS/lexidma/actions/workflows/docbook-to-markdown.yml?query=branch%3Amarkdown-conversion)

The Markdown edition of DMLex Version 1.0 OASIS Standard, and the new
[Version 1.1 Working Draft 01](../../../../dmlex-v1.1/dmlex-v1.1-wd01.md), rendered
through the OASIS publication pipeline and checked against the OASIS publication
acceptance criteria.

[![Published edition on the left, Markdown edition on the right](comparison/html-1-cover.png)](comparison/html-1-cover.png)

## Start Here

| | Report | Read it |
|---|---|---|
| **1** | **Publication audit.** 15 gates, 10 findings, verdict PASS. The one-page answer to "is the Markdown edition right?" | [PDF](dmlex-markdown-edition-publication-audit-2026-09-24.pdf) · [Word](dmlex-markdown-edition-publication-audit-2026-09-24.docx) · [Markdown](dmlex-markdown-edition-publication-audit-2026-09-24.md) · [Sources](sources/) |
| **2** | **Rendering comparison.** The published edition and the Markdown edition side by side, 7 HTML views and 5 PDF pages | [PDF](dmlex-rendering-comparison-2026-09-24.pdf) · [Word](dmlex-rendering-comparison-2026-09-24.docx) · [Pictures](comparison/) |
| **3** | **Validation, v1.1 WD01.** Every one of the 170 acceptance checks, with what was found | [PDF](dmlex-v1.1-wd01-pub-check-validation-2026-09-24.pdf) · [Word](dmlex-v1.1-wd01-pub-check-validation-2026-09-24.docx) · [JSON](dmlex-v1.1-wd01-pub-check-validation-2026-09-24.json) |
| **4** | **Validation, v1.0 OS Markdown edition.** The same checks on the published standard | [PDF](dmlex-v1.0-os-markdown-pub-check-validation-2026-09-24.pdf) · [Word](dmlex-v1.0-os-markdown-pub-check-validation-2026-09-24.docx) · [JSON](dmlex-v1.0-os-markdown-pub-check-validation-2026-09-24.json) |
| **5** | **Rendered specifications.** What the pipeline produces | [v1.1 WD01 PDF](rendered/dmlex-v1.1-wd01.pdf) · [v1.0 OS PDF](rendered/dmlex-v1.0-os.pdf) |

## Headline Numbers

| Measure | Published (DocBook) | Markdown edition |
|---|---|---|
| Words compared | 61,253 | 0 unexplained differences |
| Numbered headings | 311 | 311 |
| Code blocks | 316 | 316, all byte-identical |
| Internal links | 3,166 | 3,166, none broken |
| Figures | 49 | 49, same width |
| PDF body text | 10pt | 10pt (12pt until the 25 September fix) |
| PDF pages | 218 | 194 |

## What the TC Needs to Decide

The gate's remaining blockers are all in the published v1.0 source. The
conversion reproduces them faithfully, and they carry into v1.1 until the TC
changes them.

| | Blocker | Where | The decision |
|---|---|---|---|
| **1** | Both JSON schemas declare the same `$id`, `http://docs.oasis-open.org/lexidma/ns/dmlex-1.0`, which serves a web page, not a schema | [`dmlex-v1.1/schemas/JSON/`](../../../../dmlex-v1.1/schemas/JSON/) | The `$id` of each v1.1 schema |
| **2** | Appendix C cites `dmlex.nvh`, which is not in the repository. It holds `dmlex_model_description.nvh`, a different file | [`dmlex-v1.1/schemas/informativeCopiesOf3rdPartySchemas/NVH/`](../../../../dmlex-v1.1/schemas/informativeCopiesOf3rdPartySchemas/NVH/) | Commit the file under the cited name, or change the citation |
| **3** | The [XML Catalogs] reference in Appendix B is a member-only URL, which Naming Directives v1.7 section 6.6 does not allow in a public document | [WD01, Appendix B](../../../../dmlex-v1.1/dmlex-v1.1-wd01.md#references) | A public URL for the reference |

WD01 already fixes two typos from v1.0: the doubled `.pdf.pdf` in Appendix F,
and "OASIS OASIS Standard" in the citation.

## Side by Side

Published edition on the left, Markdown edition on the right. Select a picture
for the full size.

| HTML | |
|---|---|
| [![Table of contents](comparison/html-2-toc.png)](comparison/html-2-toc.png) Table of contents | [![Section 3.4 entry](comparison/html-3-core_entry.png)](comparison/html-3-core_entry.png) Section 3.4 `entry` |
| [![Example 15](comparison/html-4-ex15.png)](comparison/html-4-ex15.png) Example 15 | [![XML serialization](comparison/html-5-xml_entry.png)](comparison/html-5-xml_entry.png) XML serialization of `entry` |
| [![References](comparison/html-6-references.png)](comparison/html-6-references.png) Appendix B References | [![UML diagram](comparison/html-7-diagram_uml.png)](comparison/html-7-diagram_uml.png) Appendix D UML diagram |

| PDF | |
|---|---|
| [![PDF cover](comparison/pdf-1-cover.png)](comparison/pdf-1-cover.png) Cover | [![PDF contents](comparison/pdf-2-toc.png)](comparison/pdf-2-toc.png) Table of contents |
| [![PDF entry](comparison/pdf-3-entry.png)](comparison/pdf-3-entry.png) Section 3.4 `entry` | [![PDF example](comparison/pdf-4-example.png)](comparison/pdf-4-example.png) Example 6 |
| [![PDF UML](comparison/pdf-5-uml.png)](comparison/pdf-5-uml.png) Appendix D UML diagram | |

## How It Was Made

| Step | Tool |
|---|---|
| DocBook to Markdown, verified word by word against the published HTML | [`tools/docbook-to-markdown`](../../../docbook-to-markdown/) |
| Render, stage and gate each edition | [`tools/publication-assurance/render.sh`](../../render.sh) |
| The acceptance criteria | [OASIS-Docs/publication-assurance](https://github.com/OASIS-Docs/publication-assurance), [check catalogue](https://github.com/OASIS-Docs/publication-assurance/blob/main/pub-check/CHECKS.md) |
| CI on every change | [Publication assurance workflow](https://github.com/MColetta-OASIS/lexidma/actions/workflows/publication-assurance.yml?query=branch%3Amarkdown-conversion) |

For advancing the draft to WD02 or CSD01, see the
[v1.1 README](../../../../dmlex-v1.1/README.md). For running any of this
locally, see the [pipeline README](../../README.md).

---

Prepared by OASIS TC Administration as a publication service. It is not a
contribution to the TC's work product.
