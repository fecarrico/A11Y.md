// biblioteca antiga carregada mas nunca usada nesta página
function bookCard(b) {
  return `<div class="old-card"><img src="${b.img}" alt=""><a href="${b.url}">Ver</a></div>`;
}
window.LEGACY_BOOKS = [];
window.LEGACY_BOOKS.forEach(function (b) { /* nada renderiza aqui */ });
