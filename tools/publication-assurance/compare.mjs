// Side-by-side visual comparison of the published DocBook HTML and the
// Markdown edition rendered by render.sh, at a fixed set of anchors.
//
//   npm install --no-save puppeteer-core@24
//   CHROME=/path/to/chrome node tools/publication-assurance/compare.mjs \
//       PUBLISHED_URL RENDERED_HTML OUT_DIR
//
// For each anchor it scrolls both pages to the same element and captures the
// viewport, writing <n>-<anchor>-published.png and <n>-<anchor>-markdown.png.
// render.sh's compare step joins each pair into one labelled image.
import puppeteer from 'puppeteer-core';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const [published, rendered, out] = process.argv.slice(2);
const anchors = [
  ['cover', null],                       // title page and front matter
  ['toc', 'table-of-contents'],          // table of contents (DocBook: div.toc)
  ['core_entry', 'core_entry'],          // a core object type with its diagram
  ['ex15', 'ex15'],                      // a numbered example with code
  ['xml_entry', 'xml_entry'],            // XML serialization of an object type
  ['references', 'references'],          // normative references
  ['diagram_uml', 'diagram_uml'],        // Appendix D, the UML diagram
];
mkdirSync(out, { recursive: true });
const browser = await puppeteer.launch({
  executablePath: process.env.CHROME, headless: true, args: ['--no-sandbox'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1100, height: 1400, deviceScaleFactor: 1 });
const sides = [['published', published], ['markdown', 'file://' + resolve(rendered)]];
for (const [side, url] of sides) {
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 120000 });
  for (const [i, [name, id]] of anchors.entries()) {
    const found = await page.evaluate((id) => {
      if (!id) { window.scrollTo(0, 0); return true; }
      const el = document.getElementById(id) || document.querySelector(`[name="${id}"]`)
        || (id === 'table-of-contents' ? document.querySelector('div.toc') : null);
      if (!el) return false;
      el.scrollIntoView({ block: 'start' });
      window.scrollBy(0, -12);
      return true;
    }, id);
    if (!found) { console.log(`MISSING ${side} #${id}`); continue; }
    await new Promise((r) => setTimeout(r, 400));
    await page.screenshot({ path: `${out}/${i + 1}-${name}-${side}.png` });
  }
}
await browser.close();
