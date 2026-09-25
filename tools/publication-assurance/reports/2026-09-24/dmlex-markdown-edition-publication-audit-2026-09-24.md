# Publication Audit Report: DMLex v1.0 OS Markdown edition and v1.1 WD01

| Field | Value |
|---|---|
| Artifact | DMLex v1.0 OS Markdown edition and v1.1 WD01, stage os (Markdown edition) and wd01 |
| Published at | Not published. Source: https://github.com/MColetta-OASIS/lexidma/tree/markdown-conversion (fork of oasis-tcs/lexidma); comparison baseline https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.html |
| Source release | oasis-tcs/lexidma DocBook 4.5 source of DMLex v1.0 OS (dmlex-v1.0/specification), converted by tools/docbook-to-markdown |
| Publisher repo | MColetta-OASIS/lexidma @ markdown-conversion (commit recorded in the pull request that carries this report) |
| TCADMIN ticket | TCADMIN-4742 |
| Public review window | Not applicable: nothing is opened for public review |
| Audit date | 2026-09-24 |
| Audit mode | audit-only |
| Auditor | Michael Coletta, Technical Advisor, OASIS Open, with an independent adversarial verifier agent |

## Verdict

**PASS.** 15 gates: 6 pass, 0 fail, 9 not applicable. 10 finding(s).

**PENDING SIGN-OFF by Michael Coletta, Technical Advisor, OASIS Open.**

The Markdown edition reproduces the published DMLex v1.0 OASIS Standard without technical change and renders through the OASIS pipeline at the published PDF's body and footer sizes. The three rendering defects this audit found (F1, F2, F10) are fixed and verified. The remaining gate blockers, 9<sup>S2</sup> in the v1.0 edition and 5<sup>S3</sup> in WD01, all come from the published source (F3 to F6): F6 is already corrected in WD01, and F3 to F5 are the TC's to resolve in v1.1. WD01 is ready for the TC to edit.

## 1. Scope and method

The subject is the Markdown edition and its rendering, not a deployment, so every comparison was made against the published OASIS Standard, not against a staged copy. Text: verify_md.py aligned the Markdown against the live published HTML word by word (61,253<sup>S1</sup> published tokens, 0<sup>S1</sup> unexplained difference regions, 11<sup>S1</sup> accepted deviations each with a written reason), and compared every code block byte for byte, every numbered heading, every internal anchor and every image. Rendering: both editions were driven through the OASIS publication pipeline (pandoc and the OASIS post-processor, then the OASIS PDF preprocessor and headless Chrome), staged at their docs.oasis-open.org paths, and gated with oasis-pub-check v1.5.0. Type sizes were read from the text layer of each PDF with PyMuPDF, weighted by characters. Visual: seven HTML anchor pairs and five PDF page pairs were captured side by side from the live published edition and the Markdown edition, and read. Every defect the gate raised was traced to its origin in the live published HTML or schemas before it was classified. An independent verifier with a refutation mandate tested seven load-bearing claims.

## 2. Gate results

Every gate, its result, and where the evidence sits. The evidence itself follows in section 3.

| # | Gate | Result | Findings |
|---|---|---|---|
| 1 | GitHub truth (gate.py exit 0; live bytes == pushed HEAD) | NA | - |
| 1a | Live equals GitHub (HTML diff classified, e.g. Cloudflare rewrites) | NA | - |
<!-- internal-only -->
| 2 | Render class vs precedent (same TC / same toolchain) | PASS | F1, F2, F10 |
<!-- /internal-only -->
<!-- external-only -->
| 2 | Render class vs precedent (same TC / same toolchain) | PASS | - |
<!-- /external-only -->
| 3 | Front matter vs roster / companion doc / ticket | PASS | F9 |
| 3a | Stage name per CURRENT Naming Directives; no revision collision | PASS | - |
| 4 | Index chain (index_audit.py --deep exit 0) | NA | - |
| 5 | Zip + manifest byte-identical, no junk members, extras present | NA | - |
| 6a | allmembers Invitation to Comment delivered (verified at destination) | NA | - |
| 6b | TC's own HL community post live | NA | - |
| 6c | TC's -comment HL community post live | NA | - |
| 6d | Public review discoverability (open-reviews category feed) | NA | - |
| 6e | www news post live (when stage warrants one) | NA | - |
| 6f | TCADMIN ticket carries the complete verified-link record | PASS | - |
| 7 | Independent adversarial verifier (fresh agent, refute mandate) | PASS | - |
| 8 | Visual eyeball (cover + listings screenshots, Read and compared) | PASS | - |

## 3. Gate evidence

### Gate 1. GitHub truth (gate.py exit 0; live bytes == pushed HEAD)

**Result:** NA

Not applicable. Nothing is deployed to docs.oasis-open.org. The Markdown edition and WD01 live on a fork branch for the TC to review and merge.

### Gate 1a. Live equals GitHub (HTML diff classified, e.g. Cloudflare rewrites)

**Result:** NA

Not applicable. No live copy exists to compare against GitHub.

<!-- internal-only -->

### Gate 2. Render class vs precedent (same TC / same toolchain)

**Result:** PASS (see F1, F2, F10)

Precedent is the published DMLex v1.0 OS in its own DocBook render. verify_md.py against the live HTML: RESULT PASS; 0<sup>S1</sup> unexplained difference regions; all 311<sup>S1</sup> numbered headings present, 0<sup>S1</sup> missing; 316<sup>S1</sup> code blocks in each edition, 0<sup>S1</sup> differing; 3,166<sup>S1</sup> internal links, 0<sup>S1</sup> broken; 50<sup>S1</sup> images in each edition (49<sup>S5</sup> figures and the OASIS logo), 0<sup>S1</sup> missing. Rendered through the OASIS Markdown pipeline, the edition takes the OASIS Markdown template look (markdown-styles v1.7.3 stylesheet) with the published content. Three render defects were found in this audit and fixed (F1, F2, F10): figure width, PDF scale and PDF type size. After the fixes, body text prints at 10pt<sup>S4</sup> and code at 9pt<sup>S4</sup> against 10pt<sup>S4</sup> and 10pt<sup>S4</sup> in the published PDF, figures at 567px<sup>S5</sup> against 566.93px<sup>S5</sup>, and the PDF footer prints at 8pt<sup>S4</sup>, as in the published PDF. Accepted class differences: the Markdown template labels the cover URIs This/Previous/Latest stage rather than version, notes render as shaded blocks, and the table of contents is a nested list with object-type names in body type rather than monospace. The Appendix D UML diagram is regenerated from the TC's own source by the converter, so Graphviz places the boxes differently from the published SVG while the classes, attributes and relations are the same.

<!-- /internal-only -->

<!-- external-only -->

### Gate 2. Render class vs precedent (same TC / same toolchain)

**Result:** PASS

Precedent is the published DMLex v1.0 OS in its own DocBook render. verify_md.py against the live HTML: RESULT PASS; 0<sup>S1</sup> unexplained difference regions; all 311<sup>S1</sup> numbered headings present, 0<sup>S1</sup> missing; 316<sup>S1</sup> code blocks in each edition, 0<sup>S1</sup> differing; 3,166<sup>S1</sup> internal links, 0<sup>S1</sup> broken; 50<sup>S1</sup> images in each edition (49<sup>S5</sup> figures and the OASIS logo), 0<sup>S1</sup> missing. Rendered through the OASIS Markdown pipeline, the edition takes the OASIS Markdown template look (markdown-styles v1.7.3 stylesheet) with the published content. Three render defects were found in this audit and fixed (F1, F2, F10): figure width, PDF scale and PDF type size. After the fixes, body text prints at 10pt<sup>S4</sup> and code at 9pt<sup>S4</sup> against 10pt<sup>S4</sup> and 10pt<sup>S4</sup> in the published PDF, figures at 567px<sup>S5</sup> against 566.93px<sup>S5</sup>, and the PDF footer prints at 8pt<sup>S4</sup>, as in the published PDF. Accepted class differences: the Markdown template labels the cover URIs This/Previous/Latest stage rather than version, notes render as shaded blocks, and the table of contents is a nested list with object-type names in body type rather than monospace. The Appendix D UML diagram is regenerated from the TC's own source by the converter, so Graphviz places the boxes differently from the published SVG while the classes, attributes and relations are the same.

<!-- /external-only -->

### Gate 3. Front matter vs roster / companion doc / ticket

**Result:** PASS (see F9)

Cover front matter (chair, six editors with affiliations, TC name and link, additional artifacts, namespace, abstract, status, key words, citation) aligns with the published OS cover under verify_md.py, word for word apart from the accepted deviations it lists. WD01 carries the same roster unchanged; the live TC roster was not consulted, and whether the v1.1 editor list changes is a TC decision (F9).

### Gate 3a. Stage name per CURRENT Naming Directives; no revision collision

**Result:** PASS

oasis-pub-check v1.5.0 stage-name, filenames and version-naming raise nothing on either package: os and wd01 are current Naming Directives stage tokens, and the files are dmlex-v1.0-os.* and dmlex-v1.1-wd01.* in v1.0/os/ and v1.1/wd01/. The revision-collision warning on the OS package is expected: it is the published stage itself, re-rendered. No v1.1 stage exists yet, so wd01 cannot collide.

### Gate 4. Index chain (index_audit.py --deep exit 0)

**Result:** NA

Not applicable. No directory indexes are created or changed; nothing is deployed.

### Gate 5. Zip + manifest byte-identical, no junk members, extras present

**Result:** NA

Not applicable. No distribution zip or manifest is produced for an unpublished working draft or a non-authoritative edition of a published standard.

### Gate 6a. allmembers Invitation to Comment delivered (verified at destination)

**Result:** NA

Not applicable. No announcement: not a publication.

### Gate 6b. TC's own HL community post live

**Result:** NA

Not applicable. No announcement: not a publication.

### Gate 6c. TC's -comment HL community post live

**Result:** NA

Not applicable. No announcement: not a publication.

### Gate 6d. Public review discoverability (open-reviews category feed)

**Result:** NA

Not applicable. No public review is opened.

### Gate 6e. www news post live (when stage warrants one)

**Result:** NA

Not applicable. No news post warranted.

### Gate 6f. TCADMIN ticket carries the complete verified-link record

**Result:** PASS

TCADMIN-4742 (Document model) is the TC's ticket for this work; this report and both validation reports are the record filed against it.

### Gate 7. Independent adversarial verifier (fresh agent, refute mandate)

**Result:** PASS

A fresh verifier agent was given seven claims and a mandate to refute them. It confirmed six: WD01 differs from the OS Markdown only in stage-bound values and two typo fixes (git diff --no-index, five hunks); the .pdf.pdf link text, the member-only URL and the doubled 'OASIS OASIS Standard' are in the live published HTML; both JSON schemas declare the same $id, which serves an HTML redirect page, not a schema; the published dmlex.nvh is absent from the TC repository and differs from its dmlex_model_description.nvh (sha256 a974b247<sup>S6</sup> against 987ecbe5<sup>S6</sup>); all 49<sup>S5</sup> published figures carry width 566.93<sup>S5</sup> (the fiftieth published image, the OASIS logo, is 290pt<sup>S5</sup>) and all 49<sup>S5</sup> Markdown figures carry 567<sup>S5</sup>; both WD01 Previous-stage URIs return 200<sup>S12</sup>. It refuted part of the seventh: the first draft of the stage-uri-live fix could let a later stage with a mis-cited Previous stage hide a broken Latest URI. The case was reproduced as a failing test, the fix was re-keyed on whether the version root exists on the site, and the test passes in the publication-assurance v1.4.2 release (its suite, re-run on 25 September: 141<sup>S7</sup> passed).

### Gate 8. Visual eyeball (cover + listings screenshots, Read and compared)

**Result:** PASS

Twelve side-by-side captures, each read and compared, live published edition on the left and the Markdown edition on the right. HTML at seven anchors: cover and front matter, table of contents, s3.4 entry, Example 15, s5.1 XML entry, Appendix B References, Appendix D UML diagram. PDF at five pages: cover, table of contents, s3.4 entry, Example 6, Appendix D. They are reproduced in the Rendering Comparison report and committed under tools/publication-assurance/reports/2026-09-24/comparison/.

## 4. Findings

Findings about the Work Product itself, 6 of 10.

### F3. Both JSON schemas declare the same $id, and it does not resolve to a schema

**Classification:** external / major

schemas/JSON/dmlex.schema.json and dmlex_no-crosslingual.schema.json both declare $id http://docs.oasis-open.org/lexidma/ns/dmlex-1.0. That URI redirects to an HTML namespace page. Two distinct schemas sharing one $id is ambiguous to any JSON Schema processor, and an implementer following the $id does not reach either schema. oasis-pub-check blocks it in both packages.

**Impact:** Inherited from the published v1.0 OS, which cannot change. For v1.1 the TC decides the $id scheme; the conventional choice is the version-root URL of each schema file.

### F4. The cited NVH schema dmlex.nvh is not in the TC repository

**Classification:** external / major

The specification cites .../schemas/informativeCopiesOf3rdPartySchemas/NVH/dmlex.nvh. The published site serves that file (placed during the June 2026 defect fix), but the TC repository holds only dmlex_model_description.nvh, which is not the same file (sha256 987ecbe5<sup>S6</sup> against the published a974b247<sup>S6</sup>). A package rendered from the repository therefore lacks the cited file.

**Impact:** Inherited. For v1.1 the TC should commit the file it intends under the cited name, or change the citation.

### F5. Reference [XML Catalogs] cites a member-only (Kavi) URL

**Classification:** external / major

Appendix B cites https://www.oasis-open.org/committees/download.php/14809/xml-catalogs.html. Naming Directives v1.7 s6.6 bars password-protected member-only references from any TC document that is or may become public.

**Impact:** Inherited. For v1.1 the reference needs a public URL for XML Catalogs.

### F6. Change-tracking links show '.pdf.pdf' in their visible text

**Classification:** external / minor

In Appendix F the visible link text for CSD03 and CSD04 ends '.pdf.pdf' while the link targets end '.pdf'. Present in the published HTML.

**Impact:** Reproduced in the v1.0 edition, as published. Corrected in WD01 as a typo.

### F7. The citation reads 'OASIS OASIS Standard'

**Classification:** external / minor

The citation format on the published cover repeats 'OASIS'. The TC stylesheet prefixes the stage name, which already begins with OASIS.

**Impact:** Reproduced in the v1.0 edition, as published. WD01 reads 'OASIS Working Draft 01'.

### F9. WD01 content left for the TC

**Classification:** external / info

WD01 changes stage-bound values only. Left for the TC: the editor list; the RDF vocabulary namespace, which still names v1.0 (a technical decision); the sentence in section 2 (Conformance) that names DMLex Version 1.0; the JSON schema $id values (F3); and Appendix F change tracking, which describes the v1.0 drafts.

**Impact:** None until the TC edits the draft.

<!-- internal-only -->

### Findings about the publication process, 4 of 10

These concern how OASIS ran this publication rather than anything the TC submitted, and are omitted from the external form of this report.

### F1. Figures lost their published width in the Markdown edition (fixed)

**Classification:** product / minor

All 49<sup>S5</sup> figures in the DocBook source carry `contentwidth="16cm"`<sup>S5</sup>, which the TC stylesheet renders as `width="566.929133858268"`<sup>S5</sup>. The converter emitted plain Markdown images, so each SVG drew at its natural size and the Appendix D UML diagram ran off the page. The converter now emits an HTML img element with width 567<sup>S5</sup> (16cm<sup>S5</sup> at the stylesheet's 90<sup>S11</sup> dpi, rounded) and the verifier counts HTML images. verify_md.py reports RESULT PASS for the regenerated edition, and all 49<sup>S5</sup> of its figures carry the width.

**Impact:** Every figure in the edition drew at its natural size until the fix. Nothing was released with the defect.

### F2. PDF printed shrunk to fit, with no page footer (fixed)

**Classification:** product / major / remediated

Two causes. The OASIS PDF preprocessor set white-space: nowrap on inline code, so one long inline path in s3.2.1, wider than the text column, widened the page and Chrome shrank every page to fit, printing the 12pt<sup>S8</sup> body text far below its set size. Separately, the first print step used Chrome's command-line print, which carries no footer. The preprocessor now lets inline code wrap only when a span is wider than the line (publication-assurance v1.4.2, pinned by a test), and the PDF is printed through puppeteer-core with the published PDF's footer: document name and Standards Track Work Product, copyright line, date and page x of y. The published title-free header layout is kept, which also clears the gate's pdf-cover check.

**Impact:** Would have affected every Markdown-track PDF with a long inline code span, not only DMLex. Caught in render, before release.

**Exposure window:** None. Found in the first render; nothing was committed or published with the defect.

**Remediation, verified:** The text layer of both rendered PDFs spans the full 20mm<sup>S10</sup>-margin column, 57.0pt<sup>S4</sup> to 539.2pt<sup>S4</sup>, and carries a footer on all 194<sup>S4</sup> pages; pdf-cover raises nothing. The body size first reported here came from median word-box heights, which measure line boxes rather than type, and hid a 12pt<sup>S4</sup> against 10pt<sup>S4</sup> mismatch: see F10.

### F8. Two gate defects found and fixed while auditing this work

**Classification:** process / info

oasis-pub-check reported a cited directory (schemas/, schemas/JSON/) as missing even when it shipped, and blocked the first stage of every new version because its Latest-stage URI cannot exist before its own publication. Both fixed with regression tests: publication-assurance v1.4.1 (PR #8) and v1.4.2 (PR #9).

**Impact:** Every TC using the gate benefits; neither defect had produced a wrong publication.

### F10. PDF body text printed larger than in the published PDF (fixed 25 September)

**Classification:** product / major / remediated

The OASIS Markdown stylesheet (markdown-styles v1.7.3) sets 12pt<sup>S8</sup> body text, 12pt<sup>S8</sup> tables and an 18pt<sup>S8</sup> h1, and nothing in the pipeline set a print size. Headless Chrome prints CSS points one to one, so once the F2 scaling was removed the PDF printed its body at 12pt<sup>S4</sup> against 10pt<sup>S4</sup> in the published DMLex PDF, and its footer at 6pt<sup>S4</sup> against 8pt<sup>S4</sup>. The F2 check compared median word-box heights, which include line spacing, so it scored the two as equal. The OASIS PDF preprocessor now sets a print type scale in points (body 10pt<sup>S9</sup>, code 9pt<sup>S9</sup>, tables 9pt<sup>S9</sup>, headings 16pt<sup>S9</sup>, 14pt<sup>S9</sup>, 12pt<sup>S9</sup>, 11pt<sup>S9</sup> and 10pt<sup>S9</sup> for h1 to h5), keeps headings and example captions with what follows them, and holds tables to the column, for Chrome and for wkhtmltopdf (OASIS-Docs/publication-assurance v1.5.0, which this repository pins); the footer is 8pt<sup>S10,S4</sup>. It was first fixed here with a local print stylesheet on 25 September, and moved into the shared pipeline the same day so every TC's PDF gets it.

**Impact:** Every page of both rendered PDFs: 228<sup>S4</sup> pages for the v1.0 edition and 227<sup>S4</sup> for WD01, against 218<sup>S4</sup> published. The printed type size of any Markdown-track specification depended on the renderer, because the stylesheet sets screen sizes only.

**Exposure window:** 24 to 25 September 2026: the two rendered PDFs in reports/2026-09-24/rendered on the markdown-conversion branch of the fork. Nothing was published to docs.oasis-open.org.

**Remediation, verified:** Font sizes from the PDF text layer (PyMuPDF spans, share of the characters outside the footer): v1.0 OS body LiberationSans<sup>S4</sup> 10.0pt<sup>S4</sup> 44.6%<sup>S4</sup>, code CourierNewPSMT<sup>S4</sup> 9.0pt<sup>S4</sup> 41.1%<sup>S4</sup>, footer 8.0pt<sup>S4</sup>; published body ArialMT<sup>S4</sup> 10.0pt<sup>S4</sup> 46.4%<sup>S4</sup>, code Courier<sup>S4</sup> 10.0pt<sup>S4</sup> 38.4%<sup>S4</sup>, footer 8.0pt<sup>S4</sup>. 194<sup>S4</sup> pages for v1.0 OS and v1.1 WD01 alike. Two layout defects in the new render, a heading left alone above the Appendix D diagram and a code block split from its caption, were fixed by keeping headings and example captions with what follows them.

<!-- /internal-only -->

<!-- internal-only -->

## 5. Notes

Timestamps are Europe/London. The two validation reports (pub-check) are filed alongside this one: dmlex-v1.1-wd01-pub-check-validation-2026-09-24 and dmlex-v1.0-os-markdown-pub-check-validation-2026-09-24. The sources listed under Sources were produced on 25 September 2026, when this record was rebuilt.

<!-- /internal-only -->

## 6. Conclusion

The Markdown edition reproduces the published DMLex v1.0 OASIS Standard without technical change and renders through the OASIS pipeline at the published PDF's body and footer sizes. The three rendering defects this audit found (F1, F2, F10) are fixed and verified. The remaining gate blockers, 9<sup>S2</sup> in the v1.0 edition and 5<sup>S3</sup> in WD01, all come from the published source (F3 to F6): F6 is already corrected in WD01, and F3 to F5 are the TC's to resolve in v1.1. WD01 is ready for the TC to edit.

**PENDING SIGN-OFF by Michael Coletta, Technical Advisor, OASIS Open.**

## 7. Sources

Each number marked with a source id (for example S1) was checked against that source when this report was rendered.

- **S1.** `sources/verify_md-dmlex-v1.0-os.json`. Produced by (run from the repository root): `curl -fsSL https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.html -o published.html && python3 tools/docbook-to-markdown/verify_md.py dmlex-v1.0/markdown/dmlex-v1.0-os.md published.html --root dmlex-v1.0/markdown --allow tools/docbook-to-markdown/allow.json --json tools/publication-assurance/reports/2026-09-24/sources/verify_md-dmlex-v1.0-os.json`
- **S2.** `sources/pub-check-dmlex-v1.0-os.json`. Produced by (run from the repository root): `test -d pa-v1.5.0 || git clone -q --branch v1.5.0 https://github.com/OASIS-Docs/publication-assurance.git pa-v1.5.0 && PUBCHECK=0 tools/publication-assurance/render.sh dmlex-v1.0/markdown dmlex-v1.0/specification/schemas _publication pa-v1.5.0 && (cd _publication && python3 ../pa-v1.5.0/pub-check/oasis_pub_check.py lexidma/dmlex/v1.0/os --json) > tools/publication-assurance/reports/2026-09-24/sources/pub-check-dmlex-v1.0-os.json`
- **S3.** `sources/pub-check-dmlex-v1.1-wd01.json`. Produced by (run from the repository root): `test -d pa-v1.5.0 || git clone -q --branch v1.5.0 https://github.com/OASIS-Docs/publication-assurance.git pa-v1.5.0 && PUBCHECK=0 tools/publication-assurance/render.sh dmlex-v1.1 dmlex-v1.1/schemas _publication pa-v1.5.0 && (cd _publication && python3 ../pa-v1.5.0/pub-check/oasis_pub_check.py lexidma/dmlex/v1.1/wd01 --json) > tools/publication-assurance/reports/2026-09-24/sources/pub-check-dmlex-v1.1-wd01.json`
- **S4.** `sources/pdf-type.json`. Produced by (run from the repository root): `curl -fsSL https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.pdf -o published.pdf && git show d258306:tools/publication-assurance/reports/2026-09-24/rendered/dmlex-v1.0-os.pdf > os-24sep.pdf && git show d258306:tools/publication-assurance/reports/2026-09-24/rendered/dmlex-v1.1-wd01.pdf > wd01-24sep.pdf && python3 tools/publication-assurance/measure_pdf_type.py published=published.pdf v1.0-os=tools/publication-assurance/reports/2026-09-24/rendered/dmlex-v1.0-os.pdf v1.1-wd01=tools/publication-assurance/reports/2026-09-24/rendered/dmlex-v1.1-wd01.pdf v1.0-os-24sep=os-24sep.pdf v1.1-wd01-24sep=wd01-24sep.pdf > tools/publication-assurance/reports/2026-09-24/sources/pdf-type.json`
- **S5.** `sources/figure-widths.json`. Produced by (run from the repository root): `curl -fsSL https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.html -o published.html && python3 tools/publication-assurance/count_figure_widths.py dmlex-v1.0/specification dmlex-v1.0/markdown/dmlex-v1.0-os.md published.html > tools/publication-assurance/reports/2026-09-24/sources/figure-widths.json`
- **S6.** `sources/nvh-sha256.txt`. Produced by (run from the repository root): `(curl -fsSL https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/schemas/informativeCopiesOf3rdPartySchemas/NVH/dmlex.nvh | shasum -a 256 | sed 's/-$/published dmlex.nvh/'; shasum -a 256 dmlex-v1.0/specification/schemas/informativeCopiesOf3rdPartySchemas/NVH/dmlex_model_description.nvh) > tools/publication-assurance/reports/2026-09-24/sources/nvh-sha256.txt`
- **S7.** `sources/pa-v1.4.2-pytest.txt`. Produced by (run from the repository root): `git clone -q --branch v1.4.2 https://github.com/OASIS-Docs/publication-assurance.git pa-v1.4.2 && (cd pa-v1.4.2 && python3 -m pytest tests/ -q -p no:cacheprovider) > tools/publication-assurance/reports/2026-09-24/sources/pa-v1.4.2-pytest.txt`
- **S8.** `sources/markdown-styles-v1.7.3.css`. Produced by (run from the repository root): `curl -fsSL https://docs.oasis-open.org/styles/markdown-styles-v1.7.3.css -o tools/publication-assurance/reports/2026-09-24/sources/markdown-styles-v1.7.3.css`
- **S9.** `sources/pdf_preprocessor-v1.5.0.py.txt`. Produced by (run from the repository root): `test -d pa-v1.5.0 || git clone -q --branch v1.5.0 https://github.com/OASIS-Docs/publication-assurance.git pa-v1.5.0 && cp pa-v1.5.0/.github/src/pipeline/pdf_preprocessor.py tools/publication-assurance/reports/2026-09-24/sources/pdf_preprocessor-v1.5.0.py.txt`
- **S10.** `sources/print_pdf-1ceb823.mjs.txt`. Produced by (run from the repository root): `git show 1ceb823:tools/publication-assurance/print_pdf.mjs > tools/publication-assurance/reports/2026-09-24/sources/print_pdf-1ceb823.mjs.txt`
- **S11.** `sources/docbook2md-1ceb823.py.txt`. Produced by (run from the repository root): `git show 1ceb823:tools/docbook-to-markdown/docbook2md.py > tools/publication-assurance/reports/2026-09-24/sources/docbook2md-1ceb823.py.txt`
- **S12.** `sources/previous-stage-status.txt`. Produced by (run from the repository root): `for u in https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.html https://docs.oasis-open.org/lexidma/dmlex/v1.0/os/dmlex-v1.0-os.pdf; do curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' "$u"; done > tools/publication-assurance/reports/2026-09-24/sources/previous-stage-status.txt`
