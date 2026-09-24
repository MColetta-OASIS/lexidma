#!/usr/bin/env bash
# Build the DMLex Markdown edition from the DocBook source and verify it.
#
#   build.sh SPEC_DIR OUT_DIR [PUBLISHED_HTML]
#
# SPEC_DIR        dmlex-v1.0/specification in the oasis-tcs/lexidma checkout
# OUT_DIR         receives dmlex-<version>.md plus the images it references
# PUBLISHED_HTML  the published HTML to verify against (path or URL); omit to skip
#
# Needs: xmllint, python3, pandoc (verification only), curl (URL only).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SPEC="$(cd "$1" && pwd)"
OUT="$2"
PUB="${3:-}"
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

VERSION="$(sed -n 's/.*<!ENTITY version "\([^"]*\)".*/\1/p' "$SPEC/docbook/dbgenent.mod")"
STAGE="$(sed -n 's/.*<!ENTITY stage "\([^"]*\)".*/\1/p' "$SPEC/docbook/dbgenent.mod")"
NAME="dmlex-v${VERSION}-${STAGE}"
echo "building $NAME from $SPEC"

# 1. Resolve XIncludes and entities. The module files declare the DocBook DTD by
#    its public URL; a catalog points that at the local copy so nothing is fetched.
cat > "$WORK/catalog.xml" <<EOF
<?xml version="1.0"?>
<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">
  <system systemId="http://www.docbook.org/xml/4.5/docbookx.dtd" uri="file://$SPEC/docbook/docbookx.dtd"/>
  <public publicId="-//OASIS//DTD DocBook XML V4.5//EN" uri="file://$SPEC/docbook/docbookx.dtd"/>
</catalog>
EOF
( cd "$SPEC" && XML_CATALOG_FILES="$WORK/catalog.xml" \
    xmllint --xinclude --noent --loaddtd --nonet dmlex.xml > "$WORK/merged.xml" 2> "$WORK/merge.log" )
if grep -v 'validity warning\|^\s\|^\^\|^[a-z]*\s*CDATA\|failed to load external entity "schemas/informativeCopies' "$WORK/merge.log" | grep -qi 'error'; then
  cat "$WORK/merge.log"; echo "merge failed" >&2; exit 2
fi

# 1b. Appendix D embeds dmlex_uml.svg, which the TC Makefile generates from the NVH
#     model description. Rebuild it the same way (portable: python3, no GNU head).
if [ ! -f "$SPEC/dmlex_uml.svg" ]; then
  ( cd "$SPEC"
    awk '/<programlisting>/,/<\/programlisting>/' schemas/informativeCopiesOf3rdPartySchemas/NVH/dmlex_model_description.nvh \
      | tail -n +2 | sed '$d' | python3 nvh2dot.py > "$WORK/dmlex.dot.content"
    sed "s#dmlex.dot.content#$WORK/dmlex.dot.content#" dmlex.dot.m4 | m4 > "$WORK/dmlex.dot"
    dot -Tsvg < "$WORK/dmlex.dot" > dmlex_uml.svg )
  echo "generated dmlex_uml.svg"
fi

# 2. Convert.
python3 "$HERE/docbook2md.py" "$WORK/merged.xml" "$OUT/$NAME.md"

# 3. Copy every image the Markdown references, keeping its relative path.
python3 - "$OUT/$NAME.md" "$SPEC" "$OUT" <<'PY'
import os, re, shutil, sys
md, spec, out = sys.argv[1:]
n = 0
for p in sorted(set(re.findall(r'!\[[^\]]*\]\(([^)\s]+)\)', open(md, encoding='utf-8').read()))):
    if p.startswith('http'):
        continue
    src = os.path.join(spec, p)
    if not os.path.exists(src):
        sys.exit(f'image missing in source: {p}')
    os.makedirs(os.path.dirname(os.path.join(out, p)) or out, exist_ok=True)
    shutil.copy2(src, os.path.join(out, p)); n += 1
print(f'copied {n} images')
PY

# 4. Verify against the published HTML.
if [ -n "$PUB" ]; then
  if [[ "$PUB" == http* ]]; then curl -fsSL "$PUB" -o "$WORK/published.html"; PUB="$WORK/published.html"; fi
  python3 "$HERE/verify_md.py" "$OUT/$NAME.md" "$PUB" --root "$OUT" \
      --allow "$HERE/allow.json" --json "$OUT/$NAME-verification.json"
fi
