#!/usr/bin/env python3
"""Verify a converted Markdown spec against the published HTML, word by word.

Both sides are reduced to their visible text: the Markdown via pandoc (GFM ->
HTML -> text), the published HTML by stripping tags. Each side becomes a
sequence of normalised tokens and difflib aligns them. Every region where the
two disagree is reported with context, so a reviewer can see exactly which
words the conversion dropped, added or changed.

Also checks structure independently of the text:
- every heading number+title in the HTML appears in the Markdown, in order;
- every internal link target (#id) in the Markdown has an anchor;
- every code block count matches the HTML <pre> count;
- every image path exists on disk relative to --root.

Usage: verify_md.py spec.md published.html [--root DIR] [--json out.json]
Exit 0 only if every check passes.
"""
import argparse
import difflib
import html
import json
import os
import re
import subprocess
import sys


def cf_decode(hexstr):
    """Decode a Cloudflare email-obfuscation payload (first byte is the XOR key)."""
    b = bytes.fromhex(hexstr)
    return bytes(x ^ b[0] for x in b[1:]).decode('utf-8', errors='replace')


def html_text(s):
    # docs.oasis-open.org is served through Cloudflare, which replaces every email
    # address with "[email protected]" plus an encoded data-cfemail attribute.
    # Restore the address so the live page and a local copy compare the same.
    s = re.sub(r'<span class="__cf_email__" data-cfemail="([0-9a-fA-F]+)">.*?</span>',
               lambda m: cf_decode(m.group(1)), s, flags=re.S)
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)
    s = re.sub(r'<(script|style|head)[^>]*>.*?</\1>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)


def tokens(text):
    text = text.replace(' ', ' ')
    text = re.sub('[“”„″]', '"', text)
    text = re.sub('[‘’′]', "'", text)
    text = re.sub('[–—]', '-', text)
    return re.findall(r"[A-Za-z0-9À-ɏ]+|[^\sA-Za-z0-9À-ɏ]", text)


def md_to_html(md_path):
    r = subprocess.run(['pandoc', '--preserve-tabs', '-f', 'gfm', '-t', 'html', md_path],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f'pandoc failed: {r.stderr}')
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('md')
    ap.add_argument('html')
    ap.add_argument('--root', default=None, help='dir that image paths are relative to')
    ap.add_argument('--json')
    ap.add_argument('--context', type=int, default=8)
    ap.add_argument('--allow', help='JSON list of accepted deviations {published, markdown, reason}')
    ap.add_argument('--skip-front', action='store_true',
                    help='start the comparison at the first numbered section')
    a = ap.parse_args()

    md_src = open(a.md, encoding='utf-8').read()
    raw = open(a.html, 'rb').read()
    m = re.search(rb'charset=([\w-]+)', raw[:2000])
    pub = raw.decode(m.group(1).decode() if m else 'utf-8', errors='replace')
    md_html = md_to_html(a.md)

    # Drop both tables of contents: they are generated, not content.
    pub_body = re.sub(r'<div class="toc">.*?</div>\s*</div>', ' ', pub, count=1, flags=re.S)
    md_body = re.sub(r'<h1[^>]*>Table of Contents</h1>.*?<hr\s*/?>', ' ', md_html, count=1, flags=re.S)

    A = tokens(html_text(pub_body))
    B = tokens(html_text(md_body))
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    diffs = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        ctx = ' '.join(A[max(0, i1 - a.context):i1])
        diffs.append({'op': op, 'published': ' '.join(A[i1:i2]), 'markdown': ' '.join(B[j1:j2]),
                      'context_before': ctx, 'pub_pos': i1})
    accepted = []
    if a.allow:
        rules = json.load(open(a.allow))
        keep = []
        for d in diffs:
            r = next((r for r in rules if r['published'] == d['published'] and r['markdown'] == d['markdown']), None)
            if r:
                d['reason'] = r['reason']
                accepted.append(d)
            else:
                keep.append(d)
        diffs = keep
        allowed_heads = {r['published'] for r in rules if r.get('kind') == 'heading'}
    else:
        allowed_heads = set()
    matched = sum(b.size for b in sm.get_matching_blocks())
    ratio = matched / max(len(A), 1)

    # Structure: headings
    pub_heads = [re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', t))).strip()
                 for _, t in re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', pub, re.S)]
    pub_heads = [h for h in pub_heads if re.match(r'^(\d+(\.\d+)*|Appendix [A-Z]|[A-Z](\.\d+)+) ', h)]
    md_heads = [re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', t))).strip()
                for _, t in re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', md_html, re.S)]
    norm = lambda h: ' '.join(tokens(re.sub(r'^(\d+)\.(\s)', r'\1\2', re.sub(r'^Appendix ([A-Z])\.', r'Appendix \1', h)))).lower()
    md_norm = [norm(h) for h in md_heads]
    missing_heads, pos = [], 0
    for h in pub_heads:
        n = norm(h)
        try:
            pos = md_norm.index(n, pos) + 1
        except ValueError:
            if h not in allowed_heads:
                missing_heads.append(h)

    # Structure: anchors and links
    anchors = set(re.findall(r"""id=['"]([^'"]+)['"]""", md_html))
    links = re.findall(r'href="#([^"]+)"', md_html)
    broken = sorted({l for l in links if l not in anchors})

    # Code blocks
    pub_pre = len(re.findall(r'<pre[\s>]', pub))
    md_pre = len(re.findall(r'<pre[\s>]', md_html))

    # Code blocks, byte for byte in document order (whitespace at the ends trimmed)
    def pres(h):
        out = []
        for m in re.finditer(r'<pre[^>]*>(.*?)</pre>', h, re.S):
            t = html.unescape(re.sub(r'<[^>]+>', '', m.group(1)))
            out.append('\n'.join(l.rstrip() for l in t.strip('\n').split('\n')).strip())
        return out
    P, M = pres(pub), pres(md_html)
    code_mismatch = [i for i, (x, y) in enumerate(zip(P, M)) if x != y]
    if len(P) != len(M):
        code_mismatch.append(f'count {len(P)} vs {len(M)}')

    # Images
    imgs = (re.findall(r'!\[[^\]]*\]\(([^)\s]+)\)', md_src)
            + re.findall(r'<img\s[^>]*src="([^"]+)"', md_src))
    missing_imgs = []
    if a.root:
        missing_imgs = [p for p in imgs if not p.startswith('http') and not os.path.exists(os.path.join(a.root, p))]
    pub_imgs = len(re.findall(r'<img', pub))

    report = {
        'published_tokens': len(A), 'markdown_tokens': len(B), 'token_match_ratio': round(ratio, 5),
        'diff_regions': len(diffs), 'accepted_deviations': len(accepted), 'headings_published': len(pub_heads), 'headings_missing': missing_heads,
        'internal_links': len(links), 'broken_internal_links': broken,
        'code_blocks_published': pub_pre, 'code_blocks_markdown': md_pre,
        'code_blocks_differing': code_mismatch,
        'images_published': pub_imgs, 'images_markdown': len(imgs), 'images_missing_on_disk': missing_imgs,
        'diffs': diffs, 'accepted': accepted,
    }
    if a.json:
        json.dump(report, open(a.json, 'w'), indent=1, ensure_ascii=False)
    for k, v in report.items():
        if k not in ('diffs', 'accepted'):
            print(f'{k}: {v if not isinstance(v, list) else (len(v), v[:15])}')
    for d in diffs[:60]:
        print(f"\n[{d['op']}] ...{d['context_before'][-80:]}\n  PUB: {d['published'][:300]}\n  MD : {d['markdown'][:300]}")
    ok = not diffs and not missing_heads and not broken and pub_pre == md_pre and not missing_imgs and not code_mismatch
    for d in accepted:
        print(f"ACCEPTED: PUB[{d['published'][:60]}] MD[{d['markdown'][:60]}] -- {d['reason']}")
    print('\nRESULT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
