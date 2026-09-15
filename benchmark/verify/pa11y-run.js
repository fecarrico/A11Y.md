// pa11y-run.js — o segundo motor que METHODOLOGY.md registra em "Second engine,
// robustness only". HTML_CodeSniffer, independente do axe: outra base de regras,
// outra implementação. Se os dois discordarem, a discordância é reportada, não
// resolvida escolhendo o motor mais simpático.
const pa11y = require('pa11y');
const fs = require('fs'), path = require('path');
const dir = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
fs.mkdirSync(path.dirname(out), {recursive: true});
const stream = fs.createWriteStream(out, {flags: 'w'});
(async () => {
  for (const [i, f] of files.entries()) {
    let rec;
    try {
      const r = await pa11y('file://' + path.join(dir, f), {
        standard: 'WCAG2AA', runners: ['htmlcs'], timeout: 30000,
        chromeLaunchConfig: {args: ['--no-sandbox']},
      });
      const errors = r.issues.filter(x => x.type === 'error');
      rec = {id: f.replace(/\.html$/, ''), engine: 'htmlcs', errors: errors.length,
             warnings: r.issues.filter(x => x.type === 'warning').length,
             codes: [...new Set(errors.map(x => x.code))],
             detail: errors.slice(0, 40).map(x => ({code: x.code, sel: (x.selector||'').slice(0,60)}))};
    } catch (e) {
      rec = {id: f.replace(/\.html$/, ''), error: String(e.message).slice(0, 120)};
    }
    stream.write(JSON.stringify(rec) + '\n');
    if ((i + 1) % 50 === 0) console.log(`  ${i + 1}/${files.length}`);
  }
  stream.end();
  console.log(`done · ${files.length} páginas · ${out}`);
})();
