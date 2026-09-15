// EXTRAÍDO VERBATIM de benchmark/harness/index.html (§Measurement 2 do
// METHODOLOGY.md). Não editar aqui: a régua mora no harness registrado; este
// arquivo é gerado por verify/extract-checklist.py e só existe para que o
// Playwright possa injetar a mesma função nas páginas já coletadas.

/* ---- pre-registered deterministic checklist (METHODOLOGY.md §Measurement 2) ---- */
function checklist(doc, win, task) {
  const c = {};

  // native elements vs clickable divs
  const clickableDivs = doc.querySelectorAll("div[onclick],span[onclick]").length;
  c["native-buttons"] = clickableDivs === 0 ? "PASS" : `FAIL (${clickableDivs} clickable div/span)`;

  // labels programmatically associated
  const fields = [...doc.querySelectorAll("input:not([type=hidden]):not([type=submit]):not([type=button]),select,textarea")];
  const unlabeled = fields.filter(el => !(el.labels && el.labels.length) &&
    !el.getAttribute("aria-label") && !el.getAttribute("aria-labelledby"));
  c["labels-associated"] = fields.length === 0 ? "N/A"
    : unlabeled.length === 0 ? "PASS" : `FAIL (${unlabeled.length}/${fields.length} unlabeled)`;

  // dynamic feedback exposed through a live region
  const live = doc.querySelectorAll("[aria-live],[role=status],[role=alert],[role=log],output").length;
  c["live-region"] = live > 0 ? "PASS" : "FAIL (no live region in DOM)";

  // minimum 24×24 CSS px target size (SC 2.5.8) — measured on the rendered DOM
  const targets = [...doc.querySelectorAll("button,a[href],input[type=submit],input[type=button],[role=button]")];
  const small = targets.filter(el => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && (r.width < 24 || r.height < 24);
  });
  c["target-24px"] = targets.length === 0 ? "N/A"
    : small.length === 0 ? "PASS" : `FAIL (${small.length} target(s) under 24px — SC 2.5.8 exceptions need a human eye)`;

  // no redundant ARIA on native elements (ARIA Soup)
  const soup = doc.querySelectorAll("button[role=button],a[href][role=link],input[role=textbox]").length;
  c["no-aria-soup"] = soup === 0 ? "PASS" : `FAIL (${soup} redundant role(s))`;

  // task 2 only: modal focus behavior — semi-automated
  if (task === "task2") c["modal-focus"] = modalCheck(doc, win);

  return c;
}

function modalCheck(doc, win) {
  try {
    const del = [...doc.querySelectorAll("button")].find(b => /delete|excluir|apagar/i.test(b.textContent));
    if (!del) return "MANUAL (no Delete button found)";
    del.click();
    const dlg = doc.querySelector("dialog[open]") ||
      [...doc.querySelectorAll("[role=dialog],[role=alertdialog],.modal,[class*=modal],[class*=overlay]")]
        .find(el => win.getComputedStyle(el).display !== "none" && el.offsetParent !== null);
    if (!dlg) return "FAIL (dialog did not open on click)";
    const focusIn = dlg.contains(doc.activeElement);
    doc.activeElement.dispatchEvent(new win.KeyboardEvent("keydown", {key: "Escape", bubbles: true}));
    doc.dispatchEvent(new win.KeyboardEvent("keydown", {key: "Escape", bubbles: true}));
    const closed = !(doc.querySelector("dialog[open]") ||
      (win.getComputedStyle(dlg).display !== "none" && dlg.offsetParent !== null));
    const parts = [`focus moved in: ${focusIn ? "yes" : "NO"}`, `Escape closes: ${closed ? "yes" : "NO"}`];
    const verdict = focusIn && closed ? "PASS" : "FAIL";
    return `${verdict} (${parts.join(", ")}) — containment + focus return need a human tab-through`;
  } catch (e) { return `MANUAL (script could not drive the modal: ${e.message})`; }
}

window.__checklist = checklist;
