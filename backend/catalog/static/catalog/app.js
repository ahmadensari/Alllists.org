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


  /* contributor share links (plan P2.24): count a visit that came with ?ref=, and add the reader's own code to shares.
     Both stay in the browser so cached pages are identical for everyone. */
  try {
    var refm = location.search.match(/[?&]ref=([0-9a-f]{4,12})/);
    if (refm && window.fetch && !sessionStorage.getItem("al-ref-sent")) {
      sessionStorage.setItem("al-ref-sent", "1");
      fetch("/_f/ref/?ref=" + refm[1] + "&path=" + encodeURIComponent(location.pathname), { credentials: "same-origin" }).catch(function () {});
    }
    var mine = doc.querySelector("[data-ref-code]");
    if (mine) { localStorage.setItem("al-myref", mine.getAttribute("data-ref-code")); }
    var myref = localStorage.getItem("al-myref");
    if (myref) {
      doc.addEventListener("click", function (ev) {
        var a = ev.target.closest("a[href*='utm_medium%3Dshare'],a[href*='utm_medium=share']");
        if (a && a.href.indexOf("ref%3D") < 0 && a.href.indexOf("ref=") < 0) {
          a.href = a.href.replace(/(%3F|%26)utm_source%3D/g, "$1ref%3D" + myref + "%26utm_source%3D");
        }
        var c = ev.target.closest("[data-copy]");
        if (c && c.getAttribute("data-copy").indexOf("ref=") < 0) {
          c.setAttribute("data-copy", c.getAttribute("data-copy") + (c.getAttribute("data-copy").indexOf("?") < 0 ? "?" : "&") + "ref=" + myref);
        }
      }, true);
    }
  } catch (e) {}

  /* exact location: only when the person presses the button; the position is matched to a place and kept in the session */
  doc.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-geolocate]");
    if (!b || !navigator.geolocation) { return; }
    navigator.geolocation.getCurrentPosition(function (pos) {
      var src = doc.querySelector("#near-you form input[name=csrfmiddlewaretoken]");
      var f = doc.createElement("form"); f.method = "post"; f.action = (doc.documentElement.lang === "ur" ? "/ur" : "") + "/prefs/location/";
      [["csrfmiddlewaretoken", src ? src.value : ""], ["lat", pos.coords.latitude], ["lon", pos.coords.longitude], ["next", location.pathname + location.search]]
        .forEach(function (kv) { var i = doc.createElement("input"); i.type = "hidden"; i.name = kv[0]; i.value = kv[1]; f.appendChild(i); });
      doc.body.appendChild(f); f.submit();
    });
  });

  /* live search on the search page: results update as you type and focus stays in the box */
  var sq = doc.getElementById("q"), live = doc.getElementById("live-results");
  if (sq && live && window.fetch) {
    var timer = null;
    sq.addEventListener("input", function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        var form = sq.form, params = new URLSearchParams(new FormData(form)); params.set("fragment", "1");
        fetch(form.action + "?" + params.toString(), { credentials: "same-origin" })
          .then(function (r) { return r.ok ? r.text() : ""; })
          .then(function (html) { live.innerHTML = html; }).catch(function () {});
      }, 180);
    });
  }

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
        doc.querySelectorAll(".geo").forEach(function (g) { g.hidden = !navigator.geolocation; });
      }).catch(function () {});
  }
})();
