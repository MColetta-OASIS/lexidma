// HTML to PDF on the OASIS pipeline's page geometry (pdf_renderer.py in
// OASIS-Docs/publication-assurance: A4 portrait, 25mm top/bottom and 20mm side
// margins) with the footer of the published DMLex PDF: document name and
// "Standards Track Work Product" on the left, the copyright line in the
// centre, the document date and "Page x of y" on the right. There is no
// running header, as in the published PDF (a header title would also repeat
// the title on the cover page, which oasis-pub-check blocks).
//
//   CHROME=/path/to/chrome node print_pdf.mjs IN.html OUT.pdf NAME COPYRIGHT DATE
import puppeteer from 'puppeteer-core';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const [input, output, name, copyright, date] = process.argv.slice(2);
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const browser = await puppeteer.launch({
  executablePath: process.env.CHROME, headless: true, args: ['--no-sandbox'],
});
const page = await browser.newPage();
await page.goto('file://' + resolve(input), { waitUntil: 'networkidle0', timeout: 180000 });
// The print type scale (print.css) goes in last, over the OASIS stylesheet.
await page.addStyleTag({ path: resolve(dirname(fileURLToPath(import.meta.url)), 'print.css') });
const small = 'font-family: Arial, sans-serif; font-size: 8pt; color: #333; width: 100%; margin: 0 20mm;';
await page.pdf({
  path: output,
  format: 'A4',
  margin: { top: '25mm', right: '20mm', bottom: '25mm', left: '20mm' },
  printBackground: true,
  displayHeaderFooter: true,
  headerTemplate: '<span></span>',
  footerTemplate: `<div style="${small} display: flex; justify-content: space-between; align-items: flex-end;">
    <span>${esc(name)}<br>Standards Track Work Product</span><span>${esc(copyright)}</span>
    <span style="text-align: right;">${esc(date)}<br>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>`,
});
await browser.close();
