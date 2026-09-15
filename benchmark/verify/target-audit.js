// target-audit.js — exploratório: abre a caixa-preta do item target-24px do
// checklist registrado, que só reporta "N alvos abaixo de 24px". Aqui cada alvo
// é medido e classificado, inclusive contra a exceção que a própria SC 2.5.8
// prevê (alvo inline dentro de um bloco de texto), que o checklist não separa
// porque, nas palavras do harness, "exceptions need a human eye".
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const dir = path.resolve(process.argv[2]), out = path.resolve(process.argv[3]);

(async () => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  fs.mkdirSync(path.dirname(out), {recursive: true});
  const stream = fs.createWriteStream(out, {flags: 'w'});
  const browser = await chromium.launch();
  const page = await browser.newPage({viewport: {width: 1280, height: 900}});
  for (const [i, f] of files.entries()) {
    let rec;
    try {
      await page.goto('file://' + path.join(dir, f), {waitUntil: 'load', timeout: 20000});
      const targets = await page.evaluate(() => {
        const sel = 'button,a[href],input[type=submit],input[type=button],[role=button],input[type=checkbox],input[type=radio],select';
        return [...document.querySelectorAll(sel)].map(el => {
          const r = el.getBoundingClientRect();
          const cs = getComputedStyle(el);
          // inline dentro de texto: display inline e com texto irmão no bloco
          const parent = el.parentElement;
          const inlineInText = cs.display.startsWith('inline') && parent &&
            (parent.textContent || '').replace(el.textContent || '', '').trim().length > 20;
          return {
            tag: el.tagName.toLowerCase(),
            type: el.getAttribute('type') || el.getAttribute('role') || '',
            w: Math.round(r.width), h: Math.round(r.height),
            visible: r.width > 0 && r.height > 0,
            inlineInText,
            text: (el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 24),
          };
        });
      });
      rec = {id: f.replace(/\.html$/, ''), targets};
    } catch (e) { rec = {id: f.replace(/\.html$/, ''), error: String(e.message).slice(0, 120)}; }
    stream.write(JSON.stringify(rec) + '\n');
    if ((i + 1) % 150 === 0) console.log(`  ${i + 1}/${files.length}`);
  }
  await browser.close(); stream.end();
  console.log(`done · ${files.length} · ${out}`);
})();
