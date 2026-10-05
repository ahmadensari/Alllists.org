// Tiny interaction layer: copy-link buttons only. Everything else works without JavaScript.
document.addEventListener("click", function (ev) {
  var b = ev.target.closest("[data-copy]");
  if (!b || !navigator.clipboard) return;
  navigator.clipboard.writeText(b.getAttribute("data-copy")).then(function () {
    var t = b.textContent; b.textContent = "✓"; setTimeout(function () { b.textContent = t; }, 1200);
  });
});
