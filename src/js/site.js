/* Higher Heights — progressive enhancement. No dependencies. */
(function () {
  "use strict";
  var doc = document;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var conn = navigator.connection || {};
  var saveData = conn.saveData === true || /(^|-)2g$/.test(conn.effectiveType || "");
  var canPlay = !reduce && !saveData;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };

  /* ── menu ─────────────────────────────────────────────── */
  var btn = $("#menuBtn"), nav = $("#nav");
  if (btn && nav) {
    var setMenu = function (open) {
      doc.body.classList.toggle("menu-open", open);
      btn.setAttribute("aria-expanded", String(open));
      btn.textContent = open ? "Close" : "Menu";
      if (open) { var first = $("a", nav); first && first.focus(); } else { btn.focus(); }
    };
    btn.addEventListener("click", function () { setMenu(!doc.body.classList.contains("menu-open")); });
    doc.addEventListener("keydown", function (e) {
      if (!doc.body.classList.contains("menu-open")) return;
      if (e.key === "Escape") setMenu(false);
      if (e.key === "Tab") {
        var f = [btn].concat($$("a", nav));
        var i = f.indexOf(doc.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { doc.body.classList.remove("menu-open"); }); });
  }

  /* ── reveal on scroll ─────────────────────────────────── */
  var rv = $$(".reveal,.clip");
  if (!("IntersectionObserver" in window) || reduce) {
    rv.forEach(function (n) { n.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    rv.forEach(function (n) { io.observe(n); });
  }

  /* ── video helpers ────────────────────────────────────── */
  function load(v) { if (!v.src && v.dataset.src) { v.src = v.dataset.src; } }

  /* hero reel + timecode */
  var hero = $("#heroVideo"), tc = $("#tc");
  if (hero && canPlay) {
    var start = function () {
      load(hero);
      var p = hero.play(); p && p.catch && p.catch(function () {});
      var fps = 25;
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      (function tick() {
        var t = hero.currentTime || 0;
        if (tc) tc.textContent = pad(Math.floor(t / 3600)) + ":" + pad(Math.floor(t / 60) % 60) + ":" + pad(Math.floor(t) % 60) + ":" + pad(Math.floor((t % 1) * fps));
        requestAnimationFrame(tick);
      })();
    };
    if (doc.readyState === "complete") start(); else window.addEventListener("load", start);
  }

  /* tile hover previews */
  if (canPlay && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    $$(".film").forEach(function (f) {
      var v = $("video", f); if (!v) return;
      f.addEventListener("mouseenter", function () {
        load(v);
        var p = v.play();
        p && p.then && p.then(function () { f.classList.add("is-playing"); }).catch(function () {});
      });
      f.addEventListener("mouseleave", function () { f.classList.remove("is-playing"); v.pause(); });
    });
  }

  /* project player */
  $$("[data-player]").forEach(function (pl) {
    var b = $(".player__btn", pl), v = $("video", pl), img = $("img", pl);
    if (!b || !v) return;
    b.addEventListener("click", function () {
      load(v); v.hidden = false; pl.classList.add("is-live");
      if (img) img.hidden = true;
      var p = v.play(); p && p.catch && p.catch(function () {});
      v.focus();
    });
  });

  /* ── work filter ──────────────────────────────────────── */
  var grid = $("#workgrid");
  if (grid) {
    var chips = $$("[data-filter]");
    chips.forEach(function (c) {
      c.addEventListener("click", function () {
        var k = c.dataset.filter;
        chips.forEach(function (o) { o.setAttribute("aria-pressed", String(o === c)); });
        $$(".film", grid).forEach(function (f) { f.hidden = !(k === "all" || f.dataset.cat === k); });
      });
    });
  }

  /* ── enquiry form ─────────────────────────────────────── */
  var form = $("#enq");
  if (form) {
    var status = $("#status"), send = $("#send"), sent = $("#sent");
    form.elements.t && (form.elements.t.value = String(Date.now()));
    var say = function (msg, state) { status.textContent = msg; status.dataset.state = state || ""; };
    var done = function () { form.hidden = true; sent.hidden = false; sent.focus(); };
    if (/[?&]sent=1/.test(location.search)) done();

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = form.elements;
      var bad = null;
      ["name", "email", "message"].forEach(function (n) { f[n].removeAttribute("aria-invalid"); });
      if (!f.name.value.trim()) bad = f.name;
      else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.email.value.trim())) bad = f.email;
      else if (f.message.value.trim().length < 10) bad = f.message;
      if (bad) {
        bad.setAttribute("aria-invalid", "true"); bad.focus();
        say(bad === f.email ? "Please enter a valid email address so I can reply." : bad === f.name ? "Please tell me your name." : "Tell me a little more about the project (a sentence or two).", "error");
        return;
      }
      var data = {
        services: $$("input[name=services]:checked", form).map(function (i) { return i.value; }),
        message: f.message.value.trim(),
        timing: (($("input[name=timing]:checked", form) || {}).value) || "",
        budget: (($("input[name=budget]:checked", form) || {}).value) || "",
        name: f.name.value.trim(), email: f.email.value.trim(), company: f.company.value.trim(),
        website: f.website.value, t: f.t ? f.t.value : "",
        token: (form.querySelector("[name=cf-turnstile-response]") || {}).value || ""
      };
      send.disabled = true; say("Sending…", "");
      fetch("/api/enquiry", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (r) {
          if (r.ok) { done(); return; }
          send.disabled = false;
          say((r.j && r.j.error) || "Something went wrong sending that.", "error");
        })
        .catch(function () {
          send.disabled = false;
          say("Couldn't reach the server. Please email hello@higherheights.studio and I'll reply directly.", "error");
        });
    });
  }
})();
