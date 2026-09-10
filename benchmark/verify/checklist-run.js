// checklist-run.js — o desfecho co-primário nº 2 (METHODOLOGY.md §Measurement),
// rodado em lote sobre páginas já coletadas.
//
// A função de checklist NÃO é escrita aqui: é extraída verbatim do harness
// registrado por extract-checklist.py e injetada na página. Reescrevê-la para
// este contexto produziria um número parecido medindo outra coisa.
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');

const dir = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);
const CHECKLIST = fs.readFileSync(path.join(__dirname, 'checklist-registered.js'), 'utf8');
// O harness identifica a tarefa do modal como "task2"; o dataset a nomeia pelo slug.
const asTask = id => id.startsWith('destructive-confirmation-modal') ? 'task2' : 'other';

(async () => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  fs.mkdirSync(path.dirname(out), {recursive: true});
  const stream = fs.createWriteStream(out, {flags: 'w'});
  const browser = await chromium.launch();
  const page = await browser.newPage({viewport: {width: 1280, height: 900}});
  for (const [i, f] of files.entries()) {
    const id = f.replace(/\.html$/, '');
    let rec;
    try {
      await page.goto('file://' + path.join(dir, f), {waitUntil: 'load', timeout: 20000});
      await page.addScriptTag({content: CHECKLIST});
      const checks = await page.evaluate(t => window.__checklist(document, window, t), asTask(id));
      rec = {id, checklist: checks};
    } catch (e) {
      rec = {id, error: String(e.message).slice(0, 140)};
    }
    stream.write(JSON.stringify(rec) + '\n');
    if ((i + 1) % 100 === 0) console.log(`  ${i + 1}/${files.length}`);
  }
  await browser.close();
  stream.end();
  console.log(`done · ${files.length} páginas · ${out}`);
})();
