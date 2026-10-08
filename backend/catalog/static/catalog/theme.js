/* Applies the saved theme before first paint (no flash). Preferences live in the browser, not in cookies the server reads,
   so every page stays identical for everyone (rule R05). */
try { var t = localStorage.getItem("al-theme"); if (t === "dark" || t === "light") document.documentElement.setAttribute("data-theme", t); } catch (e) {}
