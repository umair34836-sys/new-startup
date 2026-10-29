// Portal front end: chunked uploads, live price estimate, confirm buttons, motion.
// Subtle motion only; none when the visitor asks for reduced motion.
(function () {
  'use strict';
  var body = document.body;
  var csrf = body.dataset.csrf;
  var base = body.dataset.base || '';

  function fmtBytes(b) {
    var u = ['B', 'KB', 'MB', 'GB', 'TB'], i = 0;
    while (b >= 1024 && i < 4) { b /= 1024; i++; }
    return (i ? b.toFixed(1) : b) + ' ' + u[i];
  }

  function post(url, data, isRaw) {
    return fetch(base + url, {
      method: 'POST', credentials: 'same-origin',
      headers: { 'X-CSRF-Token': csrf, 'Content-Type': isRaw ? 'application/octet-stream' : 'application/json' },
      body: isRaw ? data : JSON.stringify(data)
    }).then(function (r) {
      return r.json().catch(function () { return { error: 'Server error (' + r.status + ')' }; })
        .then(function (j) { j._status = r.status; return j; });
    });
  }

  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  // One file at a time, one chunk at a time: the host allows only 20 connections at once.
  async function uploadFile(file, orderId, kind, li) {
    var bar = li.querySelector('.bar > i'), state = li.querySelector('.state');
    var init = await post('/upload/init', { order_id: orderId, kind: kind, name: file.name, size: file.size });
    if (init.error) throw new Error(init.error);
    var offset = init.received || 0, chunk = init.chunk, tries = 0;
    while (offset < file.size) {
      var piece = file.slice(offset, Math.min(offset + chunk, file.size));
      var r;
      try {
        r = await post('/upload/chunk?token=' + init.token + '&offset=' + offset, piece, true);
      } catch (e) { r = { error: 'network' }; }
      if (r.error) {
        if (r.error === 'offset_mismatch') { offset = r.received; continue; }
        if (++tries > 8 || r._status === 400 || r._status === 403) throw new Error(r.error === 'network' ? 'Connection lost.' : r.error);
        state.textContent = 'Connection problem, retrying…';
        await sleep(Math.min(30000, 1000 * Math.pow(2, tries)));
        continue;
      }
      tries = 0;
      offset = r.received;
      var pct = Math.round(offset / file.size * 100);
      bar.style.width = pct + '%';
      state.textContent = pct + '%';
    }
    state.textContent = 'Checking…';
    var fin = await post('/upload/finish?token=' + init.token, {});
    if (fin.error) throw new Error(fin.error);
    state.textContent = 'Uploaded';
    li.classList.add('done');
    return fin;
  }

  document.querySelectorAll('[data-uploader]').forEach(function (zone) {
    var input = zone.querySelector('input[type=file]');
    var next = zone.nextElementSibling;
    var list = next && next.matches('[data-file-list]') ? next : zone.parentElement.querySelector('[data-file-list]');
    var queue = [], busy = false, failed = false;
    var submit = document.querySelector('[data-submit]');

    function add(files) {
      Array.prototype.forEach.call(files, function (f) {
        var li = document.createElement('li');
        li.innerHTML = '<span class="fname"></span><span class="muted"></span><span class="state">Waiting</span><span class="bar"><i></i></span>';
        li.querySelector('.fname').textContent = f.name;
        li.querySelector('.muted').textContent = fmtBytes(f.size);
        list.appendChild(li);
        if (window.portalMotion) window.portalMotion.enter(li);
        queue.push({ file: f, li: li });
      });
      run();
    }
    async function run() {
      if (busy) return;
      busy = true;
      if (submit) submit.disabled = true;
      while (queue.length) {
        var job = queue.shift();
        try { await uploadFile(job.file, zone.dataset.order, zone.dataset.kind, job.li); }
        catch (e) { failed = true; job.li.querySelector('.state').textContent = 'Failed: ' + e.message; job.li.classList.add('failed'); }
      }
      busy = false;
      if (submit) submit.disabled = false;
      if (zone.dataset.reload && !failed) location.reload();
    }
    input.addEventListener('change', function () { add(input.files); input.value = ''; });
    ['dragenter', 'dragover'].forEach(function (ev) { zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add('over'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove('over'); }); });
    zone.addEventListener('drop', function (e) { if (e.dataTransfer && e.dataTransfer.files.length) add(e.dataTransfer.files); });
    zone.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
    window.addEventListener('beforeunload', function (e) { if (busy) { e.preventDefault(); e.returnValue = ''; } });
  });

  // Live estimate: seconds x rate.
  var est = document.querySelector('[data-estimate]');
  var len = document.querySelector('[data-length]');
  if (est && len) {
    var rate = parseFloat(est.dataset.rate), cur = est.dataset.currency, out = est.querySelector('[data-estimate-value]');
    len.addEventListener('input', function () {
      var s = Math.max(0, parseInt(len.value, 10) || 0), v = s * rate;
      out.textContent = cur + ' ' + v.toLocaleString('en-US', { maximumFractionDigits: cur === 'PKR' ? 0 : 2, minimumFractionDigits: cur === 'PKR' ? 0 : 2 });
    });
  }

  document.querySelectorAll('[data-confirm]').forEach(function (b) {
    b.addEventListener('click', function (e) { if (!confirm(b.dataset.confirm)) e.preventDefault(); });
  });

  // ---- Splash: logo reveal every time the site is opened from outside (not on inside page changes).
  // Ring draws in, logo settles, letters follow; about 2.5 s. Tap skips it. Reduced motion: never shown.
  function splash(g) {
    var el = document.getElementById('splash');
    if (!el) return;
    var inside = false;
    try { inside = document.referrer !== '' && new URL(document.referrer).origin === location.origin; } catch (e) {}
    var skip = false;
    try { skip = sessionStorage.getItem('splashSkip') === '1'; } catch (e) {}
    if (inside || skip) { el.remove(); return; }
    var word = el.querySelector('.splash-word');
    word.innerHTML = word.textContent.split('').map(function (c) { return c === ' ' ? '<span>&nbsp;</span>' : '<span>' + c.replace(/[<>&]/g, '') + '</span>'; }).join('');
    var circle = el.querySelector('circle'), len = 2 * Math.PI * 75.5;
    el.hidden = false;
    g.set(circle, { strokeDasharray: len, strokeDashoffset: len });
    var tl = g.timeline({ onComplete: function () { el.remove(); } });
    tl.to(circle, { strokeDashoffset: 0, duration: 0.9, ease: 'power2.inOut' }, 0)
      .fromTo('.splash-mark', { scale: 0.6, rotation: -14, opacity: 0, filter: 'blur(8px)' },
        { scale: 1.04, rotation: 0, opacity: 1, filter: 'blur(0px)', duration: 0.55, ease: 'power3.out' }, 0.25)
      .to('.splash-mark', { scale: 1, duration: 0.16, ease: 'power1.out' }, 0.8)
      .from('.splash-word span', { y: 14, opacity: 0, duration: 0.4, stagger: 0.06, ease: 'power2.out' }, 0.8)
      .from('.splash-sub', { opacity: 0, letterSpacing: '1.2em', duration: 0.5, ease: 'power2.out' }, 1.25)
      .from('.splash-host', { opacity: 0, y: 8, duration: 0.35, ease: 'power1.out' }, 1.45)
      .fromTo('.splash-ring', { filter: 'drop-shadow(0 0 0 rgba(0,212,184,0))' },
        { filter: 'drop-shadow(0 0 14px rgba(245,166,35,.8))', duration: 0.3, yoyo: true, repeat: 1 }, 1.2)
      .to(el, { opacity: 0, scale: 1.04, duration: 0.3, ease: 'power1.in' }, '+=0.7');
    el.addEventListener('click', function () { tl.progress(1); });
  }

  // ---- Motion ----
  window.addEventListener('load', function () {
    var g = window.gsap;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!g || reduce) {
      var sp = document.getElementById('splash');
      if (sp) sp.remove();
      window.portalMotion = { enter: function () {} };
      return;
    }
    splash(g);
    window.portalMotion = { enter: function (el) { g.from(el, { opacity: 0, y: 8, duration: 0.3, ease: 'power1.out', clearProps: 'all' }); } };
    // Fade the page in on load.
    g.fromTo('#main', { opacity: 0 }, { opacity: 1, duration: 0.2, ease: 'power1.inOut' });
    // Lists come in one after another.
    document.querySelectorAll('.stagger').forEach(function (list) {
      g.from(list.children, { opacity: 0, y: 8, duration: 0.3, stagger: 0.03, ease: 'power1.out', clearProps: 'all' });
    });
    // Cards fade up as they scroll into view.
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        g.from(en.target, { opacity: 0, y: 12, duration: 0.35, ease: 'power1.out', clearProps: 'all' });
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
    // Buttons lift slightly under the pointer.
    document.querySelectorAll('.btn, .order-item').forEach(function (el) {
      el.addEventListener('mouseenter', function () { g.to(el, { y: -1, duration: 0.15, ease: 'power1.out' }); });
      el.addEventListener('mouseleave', function () { g.to(el, { y: 0, duration: 0.15, ease: 'power1.out' }); });
    });
    // Success notice: slide in with a small settle.
    g.fromTo('.notice.ok', { x: -12, opacity: 0 }, { x: 0, opacity: 1, duration: 0.35, ease: 'back.out(2)' });
    // New version ready: one soft glow on the player card.
    g.fromTo('video.player', { boxShadow: '0 0 0 0 rgba(255,46,147,0)' }, { boxShadow: '0 0 0 6px rgba(255,46,147,.35)', duration: 0.5, yoyo: true, repeat: 1, delay: 0.4 });
    // Progress steps fill one after another.
    g.from('.progress li.done', { scaleX: 0.6, opacity: 0, duration: 0.3, stagger: 0.08, ease: 'power1.out', clearProps: 'all' });
  });

  // ---- App update ("OTA"). The app (TWA) opens /orders?src=twa&v=<versionCode>; remember the installed version.
  // Website changes need no update. When the owner publishes a newer APK, the app shows an update bar.
  (function () {
    var m = document.cookie.match(/(?:^|;\s*)appV=(\d+)/), installed = m ? m[1] : null;
    if (installed === null) return;
    document.querySelectorAll('[data-app-link]').forEach(function (a) { a.closest('.app-get').remove(); });
    var latest = parseInt(body.dataset.appVersion || '0', 10);
    var dismissed = false;
    try { dismissed = sessionStorage.getItem('appUpdateLater') === String(latest); } catch (e) {}
    if (latest <= parseInt(installed, 10) || dismissed) return;
    var bar = document.createElement('div');
    bar.className = 'update-bar';
    bar.setAttribute('role', 'status');
    bar.innerHTML = '<span><strong>New app version</strong> <small></small></span><a class="btn primary"></a><button class="link" type="button">Later</button>';
    bar.querySelector('small').textContent = body.dataset.appNotes || '';
    var a = bar.querySelector('a');
    a.textContent = 'Update';
    a.href = base + '/app/download';
    bar.querySelector('button').addEventListener('click', function () {
      try { sessionStorage.setItem('appUpdateLater', String(latest)); } catch (e) {}
      bar.remove();
    });
    document.body.appendChild(bar);
    if (window.gsap && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      window.gsap.from(bar, { y: 80, opacity: 0, duration: 0.4, ease: 'back.out(1.6)', delay: 0.6 });
    }
  })();

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register(base + '/sw.js').catch(function () {});
  }
})();
