/**
 * target-prepass.js — mechanical half of the SC 2.5.8 MANUAL items.
 *
 * The registered protocol: "automated where a scripted browser can decide
 * them; the remainder adjudicated by a human." A scripted browser CAN decide
 * "no interactive target below 24×24 CSS px exists on this page"; it CANNOT
 * decide the exception judgments (equivalent control, inline, essential).
 * This script measures every visible interactive target on every adjudication
 * page and reports, per page, the sub-24px targets grouped by shape — the
 * human judges exceptions only where small targets actually exist.
 *
 *   node target-prepass.js --dir <pages> --out <json>
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const args = process.argv.slice(2);
function arg(name, dflt) {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : dflt;
}
const dir = path.resolve(arg('--dir'));
const out = path.resolve(arg('--out'));

const SELECTOR = [
  'a[href]', 'button', 'input:not([type=hidden])', 'select', 'textarea',
  'summary', '[onclick]', '[tabindex]:not([tabindex="-1"])',
  '[role=button]', '[role=link]', '[role=checkbox]', '[role=radio]',
  '[role=tab]', '[role=menuitem]', '[role=option]', '[role=switch]',
].join(',');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const report = {};
  const files = fs.readdirSync(dir).filter(f => /\.html?$/i.test(f)).sort();
  for (const f of files) {
    const url = 'file://' + path.join(dir, f);
    const entry = { targets: 0, small: [], error: null };
    try {
      await page.goto(url, { waitUntil: 'load', timeout: 30000 });
      await page.waitForTimeout(400); // JS de construção da página
      const found = await page.evaluate((sel) => {
        const seen = new Set();
        const rows = [];
        for (const el of document.querySelectorAll(sel)) {
          if (seen.has(el)) continue;
          seen.add(el);
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          const r = el.getBoundingClientRect();
          if (r.width === 0 || r.height === 0) continue;
          const label = (el.getAttribute('aria-label') || el.textContent || el.value || '')
            .trim().replace(/\s+/g, ' ').slice(0, 40);
          const inline = cs.display.startsWith('inline') && el.closest('p,li,td,figcaption') !== null;
          rows.push({ tag: el.tagName.toLowerCase(), w: Math.round(r.width),
                      h: Math.round(r.height), label, inline });
        }
        return rows;
      }, SELECTOR);
      entry.targets = found.length;
      const groups = {};
      for (const t of found) {
        if (t.w >= 24 && t.h >= 24) continue;
        const key = `${t.tag} ${t.w}×${t.h}${t.inline ? ' (inline em texto)' : ''}`;
        groups[key] = groups[key] || { count: 0, exemplo: t.label };
        groups[key].count++;
      }
      entry.small = Object.entries(groups)
        .map(([shape, g]) => ({ shape, count: g.count, exemplo: g.exemplo }));
    } catch (e) {
      entry.error = String(e).slice(0, 200);
    }
    report[f] = entry;
    const n = entry.small.reduce((s, g) => s + g.count, 0);
    console.log(`${f}  alvos:${entry.targets}  sub-24px:${n}${entry.error ? '  ERRO' : ''}`);
  }
  await browser.close();
  fs.writeFileSync(out, JSON.stringify(report, null, 1));
})();
