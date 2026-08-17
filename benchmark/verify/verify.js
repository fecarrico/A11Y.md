#!/usr/bin/env node
/**
 * verify.js — headless verification: the pinned axe over every generation,
 * a screenshot of each page as a by-product of the same pass.
 *
 * The instrument is the registered one: harness/axe.min.js, SHA-256-checked
 * against axe.lock before anything runs. Pages are served over HTTP (file://
 * changes how some pages behave) and mounted unmodified. Results append to a
 * JSONL — one line per page, written before the next page loads, so a crash
 * costs one page, never the batch.
 *
 *   node verify.js --dir ../runs/html --out ../runs/verify/axe.jsonl \
 *                  --shots ../runs/verify/screenshots [--resume]
 *
 * Repeatable --dir. Only dependency: playwright (see package.json).
 */

const { chromium } = require('playwright');
const crypto = require('crypto');
const fs = require('fs');
const http = require('http');
const path = require('path');

function args() {
  const a = { dirs: [], out: null, shots: null, resume: false, timeout: 30000 };
  const v = process.argv.slice(2);
  for (let i = 0; i < v.length; i++) {
    if (v[i] === '--dir') a.dirs.push(path.resolve(v[++i]));
    else if (v[i] === '--out') a.out = path.resolve(v[++i]);
    else if (v[i] === '--shots') a.shots = path.resolve(v[++i]);
    else if (v[i] === '--resume') a.resume = true;
    else if (v[i] === '--timeout') a.timeout = parseInt(v[++i], 10);
    else { console.error(`unknown arg: ${v[i]}`); process.exit(2); }
  }
  if (!a.dirs.length || !a.out) {
    console.error('usage: node verify.js --dir DIR [--dir DIR2] --out FILE.jsonl [--shots DIR] [--resume]');
    process.exit(2);
  }
  return a;
}

function checkAxe() {
  const dir = path.resolve(__dirname, '..', 'harness');
  const lock = fs.readFileSync(path.join(dir, 'axe.lock'), 'utf8');
  const version = (lock.match(/version:\s*(\S+)/) || [])[1];
  const expected = (lock.match(/sha256:\s*([0-9a-f]{64})/) || [])[1];
  const source = fs.readFileSync(path.join(dir, 'axe.min.js'));
  const actual = crypto.createHash('sha256').update(source).digest('hex');
  if (actual !== expected) {
    console.error(`axe.min.js does not match axe.lock (${actual} != ${expected})`);
    process.exit(1);
  }
  return { source: source.toString('utf8'), version };
}

function serve(dirs) {
  // /0/<file>, /1/<file> — one prefix per --dir, nothing else reachable.
  return http.createServer((req, res) => {
    const m = req.url.match(/^\/(\d+)\/(.+)$/);
    const dir = m && dirs[Number(m[1])];
    const file = dir && path.join(dir, decodeURIComponent(m[2]));
    if (!file || !file.startsWith(dir) || !fs.existsSync(file)) {
      res.writeHead(404).end();
      return;
    }
    res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
    res.end(fs.readFileSync(file));
  });
}

(async () => {
  const a = args();
  const axe = checkAxe();

  const done = new Set();
  if (a.resume && fs.existsSync(a.out)) {
    for (const line of fs.readFileSync(a.out, 'utf8').split('\n')) {
      if (line.trim()) done.add(JSON.parse(line).id);
    }
  }

  const jobs = [];
  a.dirs.forEach((dir, index) => {
    for (const name of fs.readdirSync(dir).sort()) {
      if (!/\.html?$/i.test(name)) continue;
      const id = name.replace(/\.html?$/i, '');
      if (!done.has(id)) jobs.push({ id, url: `/${index}/${name}`, dir });
    }
  });
  console.log(`${jobs.length} page(s) to verify · axe ${axe.version} (SHA ok)` +
              (done.size ? ` · ${done.size} already done` : ''));
  if (!jobs.length) process.exit(0);

  fs.mkdirSync(path.dirname(a.out), { recursive: true });
  if (a.shots) fs.mkdirSync(a.shots, { recursive: true });

  const server = serve(a.dirs);
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  const port = server.address().port;

  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });

  let failures = 0;
  for (const [i, job] of jobs.entries()) {
    const started = Date.now();
    const record = { id: job.id, axe_version: axe.version,
                     verified_at: new Date().toISOString() };
    const page = await context.newPage();
    try {
      await page.goto(`http://127.0.0.1:${port}${job.url}`,
                      { waitUntil: 'load', timeout: a.timeout });
      await page.waitForTimeout(500); // settle: entry animations, initial JS
      await page.addScriptTag({ content: axe.source });
      const result = await page.evaluate(async () =>
        await axe.run(document, { resultTypes: ['violations'] }));

      const counts = { critical: 0, serious: 0, moderate: 0, minor: 0 };
      record.violations = result.violations.map(v => ({
        id: v.id, impact: v.impact, nodes: v.nodes.length,
      }));
      for (const v of result.violations) {
        if (counts[v.impact] !== undefined) counts[v.impact] += v.nodes.length;
      }
      record.counts = counts;

      if (a.shots) {
        const shot = path.join(a.shots, `${job.id}.png`);
        await page.screenshot({ path: shot, fullPage: true });
        record.screenshot = path.basename(shot);
      }
    } catch (error) {
      failures++;
      record.error = String(error).slice(0, 300);
    } finally {
      await page.close();
    }
    record.ms = Date.now() - started;
    fs.appendFileSync(a.out, JSON.stringify(record) + '\n');
    const c = record.counts;
    console.log(`[${i + 1}/${jobs.length}] ${job.id}` + (record.error
      ? `  ERROR ${record.error.slice(0, 60)}`
      : `  crit ${c.critical} · serious ${c.serious} · mod ${c.moderate} · minor ${c.minor}`));
  }

  await browser.close();
  server.close();
  console.log(`\ndone · ${jobs.length} page(s) · ${failures} error(s) · ${a.out}`);
  process.exit(failures ? 1 : 0);
})();
