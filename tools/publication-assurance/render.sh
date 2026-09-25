#!/usr/bin/env bash
# Render the Markdown edition of DMLex through the OASIS publication pipeline,
# stage it exactly as it would be laid out on docs.oasis-open.org, and run the
# OASIS publication gate (oasis-pub-check) against the staged package.
#
#   tools/publication-assurance/render.sh MD_DIR SCHEMAS_DIR OUT_ROOT [PA_DIR]
#
# MD_DIR       dmlex-v1.0/markdown (the .md and the images it references)
# SCHEMAS_DIR  dmlex-v1.0/specification/schemas (staged as <stage>/schemas)
# OUT_ROOT     receives the staged tree, e.g. OUT_ROOT/lexidma/dmlex/v1.0/os/
# PA_DIR       a checkout of OASIS-Docs/publication-assurance; cloned at
#              $PA_REF (default v1.5.0) into a temp dir when omitted
#
# The publish path is read from the "This stage" URL in the Markdown front
# matter, so the stage directory, filenames and URLs are the ones the gate
# checks against each other. Exit status is the gate's: 0 publishable,
# 1 blockers present. PUBCHECK=0 skips the gate (CI runs it through the
# OASIS-Docs/publication-assurance action instead).
#
# Requires pandoc 3.x, python3 with beautifulsoup4, Node.js 18+ (puppeteer-core
# is installed next to this script on first run) and Chrome or Chromium (set
# CHROME to override discovery).
set -euo pipefail

MD_DIR=$(cd "$1" && pwd)
SCHEMAS=$(cd "$2" && pwd)
mkdir -p "$3"; OUT=$(cd "$3" && pwd)
PA_REF=${PA_REF:-v1.5.0}
if [ -n "${4:-}" ]; then
  PA=$(cd "$4" && pwd)
else
  PA=$(mktemp -d)/publication-assurance
  git clone -q --depth 1 --branch "$PA_REF" https://github.com/OASIS-Docs/publication-assurance.git "$PA"
fi

MD=$(ls "$MD_DIR"/*.md | grep -v "/README.md$" | head -1)
NAME=$(basename "$MD" .md)
THIS_URL=$(grep -m1 -oE "https://docs\.oasis-open\.org/[^ ]*/$NAME\.html" "$MD")
REL=${THIS_URL#https://docs.oasis-open.org/}; REL=${REL%/*}
STAGE="$OUT/$REL"
echo "Staging $NAME at $REL"

# 1. Stage the source, the images it references and the schemas.
mkdir -p "$STAGE"
rsync -a --delete --exclude '*-verification.json' --exclude README.md --exclude schemas "$MD_DIR"/ "$STAGE"/
rsync -a "$SCHEMAS"/ "$STAGE/schemas/"

# 2. Markdown to HTML: the OASIS Stage 1 conversion (pandoc with the OASIS
#    stylesheet, then the OASIS post-processor). OUT is passed as the repo
#    base so the converter resolves the document's own publish URL. The
#    Markdown is generated and verified, so prettier (--md-format) is not run.
( cd "$STAGE" && python3 "$PA/.github/src/step_1_markdown_to_html_converter_V3_0.py" \
    "$STAGE/$NAME.md" "$OUT" "$STAGE" --md-to-html > "$OUT/stage1.log" 2>&1 ) || {
  cat "$OUT/stage1.log" >&2; echo "Stage 1 (Markdown to HTML) failed" >&2; exit 1; }
rm -f "$STAGE/markdown_conversion.log"
rmdir "$STAGE/images" 2>/dev/null || true
test -s "$STAGE/$NAME.html"

# 3. HTML to PDF: the OASIS Stage 2 preprocessor, then headless Chrome
#    print-to-PDF (the current production renderer), driven through
#    puppeteer-core so each page carries the published PDF's footer.
python3 "$PA/.github/src/fix_html_for_pdf.py" "$STAGE/$NAME.html" -o "$STAGE/.$NAME-pdf.html" > "$OUT/stage2.log" 2>&1
if [ -z "${CHROME:-}" ]; then
  for c in google-chrome chromium chromium-browser "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; do
    command -v "$c" >/dev/null 2>&1 && CHROME=$c && break
  done
fi
# puppeteer needs an absolute path, not a command name.
CHROME=$(command -v "$CHROME" || echo "$CHROME")
export CHROME
HERE=$(cd "$(dirname "$0")" && pwd)
[ -d "$HERE/node_modules/puppeteer-core" ] || npm install --prefix "$HERE" --no-save --silent puppeteer-core@24
DOC_DATE=$(grep -m1 -oE '^## [0-9]{1,2} [A-Z][a-z]+ [0-9]{4}$' "$STAGE/$NAME.md" | sed 's/^## //')
node "$HERE/print_pdf.mjs" "$STAGE/.$NAME-pdf.html" "$STAGE/$NAME.pdf" "$NAME" \
  "Copyright © OASIS Open ${DOC_DATE##* }. All Rights Reserved." "$DOC_DATE"
rm -f "$STAGE/.$NAME-pdf.html"
test -s "$STAGE/$NAME.pdf"

# 4. The publication gate. Exit 0 means publishable (warnings do not fail).
echo "Staged: $STAGE"
[ "${PUBCHECK:-1}" = 0 ] && exit 0
python3 "$PA/pub-check/oasis_pub_check.py" "$STAGE"
