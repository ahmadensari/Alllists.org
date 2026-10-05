/* Small interaction layer, no libraries (plan 8.4). Every feature is an enhancement; pages work without it. */
(function () {
  "use strict";
  var doc = document, root = doc.documentElement;

  function store(k, v) { try { if (v === undefined) { return localStorage.getItem(k); } localStorage.setItem(k, v); } catch (e) { return null; } }
  function toast(msg) {
    var el = doc.getElementById("toast"); if (!el) { return; }
    el.textContent = msg; el.classList.add("show");
    setTimeout(function () { el.classList.remove("show"); }, 1600);
  }

  /* theme toggle */
  var tt = doc.querySelector("[data-theme-toggle]");
  if (tt) {
    tt.addEventListener("click", function () {
      var cur = root.getAttribute("data-theme") ||
        (window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      var next = cur === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next); store("al-theme", next);
    });
  }

  /* list or cards view */
  var target = doc.querySelector("[data-view-target]");
  function setView(v) {
    if (!target) { return; }
    target.classList.toggle("cards", v === "cards");
    doc.querySelectorAll("[data-view]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-view") === v)); });
  }
  if (target) {
    setView(store("al-view") === "cards" ? "cards" : "list");
    doc.querySelectorAll("[data-view]").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = b.getAttribute("data-view");
        var go = function () { setView(v); store("al-view", v); };
        if (doc.startViewTransition && !(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches)) { doc.startViewTransition(go); } else { go(); }
      });
    });
  }

  /* share: native button appears only where the browser supports it; copy link copies the clean address */
  doc.querySelectorAll("[data-native-share]").forEach(function (b) {
    if (navigator.share) {
      b.hidden = false;
      b.addEventListener("click", function () { navigator.share({ title: b.getAttribute("data-title"), url: b.getAttribute("data-url") }).catch(function () {}); });
    }
  });
  var copied = (doc.currentScript && doc.currentScript.getAttribute("data-copied")) || "Copied";
  doc.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-copy]");
    if (!b || !navigator.clipboard) { return; }
    navigator.clipboard.writeText(b.getAttribute("data-copy")).then(function () { toast(copied); });
  });

  /* fragments: one private request per page brings the near-you strip, details for this viewer, the subscriber panel and
     the ad slot. Each returned element replaces the page element with the same id. */
  var holder = doc.getElementById("page-fragments");
  if (holder && window.fetch) {
    fetch(holder.getAttribute("data-fragment") + (holder.getAttribute("data-fragment").indexOf("?") < 0 ? "?" : "&") + "_=1", { credentials: "same-origin" })
      .then(function (r) { return r.status === 200 ? r.text() : ""; })
      .then(function (html) {
        if (!html) { return; }
        var tpl = doc.createElement("template"); tpl.innerHTML = html;
        tpl.content.querySelectorAll("[id]").forEach(function (n) {
          var old = doc.getElementById(n.id);
          if (old && old.parentNode) { old.replaceWith(n); }
        });
      }).catch(function () {});
  }
})();
