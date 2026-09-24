# DMLex Version 1.1 Working Draft 01

`dmlex-v1.1-wd01.md` is the starting point for DMLex Version 1.1. It is the
Markdown edition of the DMLex Version 1.0 OASIS Standard
(`dmlex-v1.0/markdown/dmlex-v1.0-os.md`) with the stage-bound values moved to
v1.1 WD01 and nothing else changed:

- the title version, the stage line (Working Draft 01) and the date
- the This, Previous and Latest stage URLs; the Previous stage is the v1.0
  OASIS Standard
- the citation label and citation
- the ten schema URLs under Additional artifacts and Appendix C
- two typos carried from the v1.0 source: the doubled `.pdf.pdf` in the
  Appendix F link text, and "OASIS OASIS Standard" in the citation

`schemas/` is a copy of the v1.0 schemas, and the figures are those of the
v1.0 edition.

## Advancing the stage

Markdown has no entities, so the stage lives in the text. To make WD02 or
CSD01, rename the file to match the stage (`dmlex-v1.1-wd02.md`) and change
the stage line, the date, the This stage URLs, the citation and the schema
URLs. Searching for `v1.1/wd01` finds every one. The publication gate checks
the stage, the URLs and the filename against each other, so anything missed
fails the `Publication assurance` workflow before it reaches OASIS.

## For the TC

The publication gate currently reports these, all carried from v1.0:

- Both JSON schemas declare `$id` `http://docs.oasis-open.org/lexidma/ns/dmlex-1.0`,
  which does not resolve to a schema.
- Appendix C cites `schemas/informativeCopiesOf3rdPartySchemas/NVH/dmlex.nvh`,
  which is not in this repository (it holds `dmlex_model_description.nvh`).
- The [XML Catalogs] reference in Appendix B is a member-only URL.

Still describing v1.0: the editor list, the RDF vocabulary namespace, the
sentence in section 2 (Conformance) that names DMLex Version 1.0, and the
Appendix F change tracking.

Render and check it locally with
`tools/publication-assurance/render.sh dmlex-v1.1 dmlex-v1.1/schemas _publication`.
See `tools/publication-assurance/README.md`.
