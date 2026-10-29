// Portal front end: chunked uploads, live price estimate, confirm buttons, motion.
// Motion presets from UI UX Pro Max data/motion.csv: #1 hover micro-interaction (subtle),
// #4 scroll reveal (subtle), #7 stagger list (subtle), #10 page transition (subtle). Reduced motion = no motion.
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
    var list = zone.parentElement.querySelector('[data-file-list]');
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

  // ---- Motion (GSAP 3.14.2, vendored from library/vendor) ----
  window.addEventListener('load', function () {
    var g = window.gsap;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!g || reduce) { window.portalMotion = { enter: function () {} }; return; }
    window.portalMotion = { enter: function (el) { g.from(el, { opacity: 0, y: 8, duration: 0.3, ease: 'power1.out', clearProps: 'all' }); } };
    // #10 page transition (subtle): fade the page in on load.
    g.fromTo('#main', { opacity: 0 }, { opacity: 1, duration: 0.2, ease: 'power1.inOut' });
    // #7 stagger list (subtle).
    document.querySelectorAll('.stagger').forEach(function (list) {
      g.from(list.children, { opacity: 0, y: 8, duration: 0.3, stagger: 0.03, ease: 'power1.out', clearProps: 'all' });
    });
    // #4 scroll reveal (subtle), with IntersectionObserver instead of ScrollTrigger (one less plugin).
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        g.from(en.target, { opacity: 0, y: 12, duration: 0.35, ease: 'power1.out', clearProps: 'all' });
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
    // #1 hover micro-interaction (subtle): lift under 2 px.
    document.querySelectorAll('.btn, .order-item').forEach(function (el) {
      el.addEventListener('mouseenter', function () { g.to(el, { y: -1, duration: 0.15, ease: 'power1.out' }); });
      el.addEventListener('mouseleave', function () { g.to(el, { y: 0, duration: 0.15, ease: 'power1.out' }); });
    });
    // Progress steps fill one after another.
    g.from('.progress li.done', { scaleX: 0.6, opacity: 0, duration: 0.3, stagger: 0.08, ease: 'power1.out', clearProps: 'all' });
  });

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register(base + '/sw.js').catch(function () {});
  }
})();
