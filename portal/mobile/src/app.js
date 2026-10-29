// MrCopper804 native app (Capacitor). The whole UI ships inside the APK; the portal API is only used for data.
// Offline: cached orders/messages, saved videos, drafts and files kept on the phone, and an outbox that syncs
// itself when the internet comes back.
(function () {
  'use strict';
  var ZERO_DEC = ['PKR', 'INR', 'NPR', 'BDT', 'LKR', 'JPY', 'KRW', 'IDR', 'VND'];
  var API = (window.PORTAL_API || '').replace(/\/$/, '');
  var CAP = window.Capacitor && window.Capacitor.Plugins ? window.Capacitor.Plugins : {};
  var isNative = !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform());
  var main = document.getElementById('main');
  var state = { token: null, user: null, cfg: null, online: navigator.onLine, syncing: false };
  var BUNDLE = window.APP_BUNDLE_VERSION || '0.0.0';

  // ---------- helpers ----------
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function money(v, cur) {
    return cur + ' ' + Number(v || 0).toLocaleString('en-US', { maximumFractionDigits: ZERO_DEC.indexOf(cur) >= 0 ? 0 : 2, minimumFractionDigits: ZERO_DEC.indexOf(cur) >= 0 ? 0 : 2 });
  }
  function bytes(b) {
    var u = ['B', 'KB', 'MB', 'GB'], i = 0;
    while (b >= 1024 && i < 3) { b /= 1024; i++; }
    return (i ? b.toFixed(1) : b) + ' ' + u[i];
  }
  function when(utc) {
    if (!utc) return '';
    var d = new Date(utc.replace(' ', 'T') + 'Z');
    return d.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
  }
  function toast(msg, type) {
    var t = document.createElement('p');
    t.className = 'notice toast ' + (type || 'ok');
    t.setAttribute('role', 'status');
    t.textContent = msg;
    document.body.appendChild(t);
    if (window.gsap && !reduced()) window.gsap.fromTo(t, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: 'back.out(2)' });
    setTimeout(function () { t.remove(); }, 3500);
  }
  function reduced() { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function uid() { return 'L' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }

  // ---------- storage: localStorage for small things, IndexedDB for blobs and caches ----------
  var ls = {
    get: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) {} }
  };
  var dbp = null;
  function db() {
    if (dbp) return dbp;
    dbp = new Promise(function (res, rej) {
      var r = indexedDB.open('mrcopper804', 1);
      r.onupgradeneeded = function () {
        var d = r.result;
        d.createObjectStore('cache');
        d.createObjectStore('drafts', { keyPath: 'lid' });
        d.createObjectStore('files', { keyPath: 'fid' });
        d.createObjectStore('outbox', { keyPath: 'id' });
        d.createObjectStore('videos');
      };
      r.onsuccess = function () { res(r.result); };
      r.onerror = function () { rej(r.error); };
    });
    return dbp;
  }
  function tx(store, mode, fn) {
    return db().then(function (d) {
      return new Promise(function (res, rej) {
        var t = d.transaction(store, mode), s = t.objectStore(store), out;
        var r = fn(s);
        if (r) r.onsuccess = function () { out = r.result; };
        t.oncomplete = function () { res(out); };
        t.onerror = function () { rej(t.error); };
        t.onabort = function () { rej(t.error); };
      });
    });
  }
  var idb = {
    get: function (st, k) { return tx(st, 'readonly', function (s) { return s.get(k); }); },
    put: function (st, v, k) { return tx(st, 'readwrite', function (s) { return k === undefined ? s.put(v) : s.put(v, k); }); },
    del: function (st, k) { return tx(st, 'readwrite', function (s) { return s.delete(k); }); },
    all: function (st) { return tx(st, 'readonly', function (s) { return s.getAll(); }); },
    clear: function (st) { return tx(st, 'readwrite', function (s) { return s.clear(); }); }
  };

  // ---------- API ----------
  function api(method, path, body, raw) {
    var h = {};
    if (state.token) h.Authorization = 'Bearer ' + state.token;
    if (body !== undefined && !raw) h['Content-Type'] = 'application/json';
    if (raw) h['Content-Type'] = 'application/octet-stream';
    return fetch(API + '/api/v1' + path, { method: method, headers: h, body: raw ? body : (body === undefined ? undefined : JSON.stringify(body)) })
      .then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (r.status === 401 && j.auth === false) { logoutLocal(); throw new Error(j.error || 'Please log in again.'); }
          if (!r.ok) { var e = new Error(j.error || ('Error ' + r.status)); e.status = r.status; e.data = j; throw e; }
          return j;
        });
      });
  }
  function isNetErr(e) { return e && (e.name === 'TypeError' || /Failed to fetch|NetworkError|network/i.test(e.message)) && !e.status; }

  // ---------- online / offline ----------
  function setOnline(v) {
    state.online = v;
    var bar = document.getElementById('netbar');
    bar.hidden = v;
    bar.textContent = 'Offline: you can keep working. Everything is sent when the internet is back.';
    if (v) sync();
  }
  window.addEventListener('online', function () { setOnline(true); });
  window.addEventListener('offline', function () { setOnline(false); });
  if (CAP.Network) {
    CAP.Network.addListener('networkStatusChange', function (s) { setOnline(!!s.connected); });
  }

  // ---------- sync engine (outbox) ----------
  function outboxAdd(item) {
    item.id = item.id || uid();
    item.created = Date.now();
    return idb.put('outbox', item).then(function () { sync(); });
  }
  function uploadBlob(orderId, rec, onProgress) {
    var init = rec.up ? Promise.resolve(rec.up) : api('POST', '/upload/init', { order_id: orderId, name: rec.name, size: rec.size }).then(function (r) {
      rec.up = { token: r.token, chunk: r.chunk };
      return idb.put('files', rec).then(function () { return rec.up; });
    });
    return init.then(function (up) {
      var offset = rec.offset || 0;
      function step() {
        if (offset >= rec.size) return api('POST', '/upload/finish?token=' + up.token, {});
        return api('POST', '/upload/chunk?token=' + up.token + '&offset=' + offset, rec.blob.slice(offset, offset + up.chunk), true)
          .catch(function (e) { if (e.data && e.data.error === 'offset_mismatch') return { received: e.data.received }; throw e; })
          .then(function (r) {
            offset = r.received;
            rec.offset = offset;
            if (onProgress) onProgress(offset / rec.size);
            return idb.put('files', rec).then(step);
          });
      }
      return step();
    });
  }
  // Drafts made on the phone: create on server -> upload files -> save (and submit if asked).
  function syncDraft(d) {
    var p = d.serverId ? Promise.resolve() : api('POST', '/orders', {}).then(function (r) { d.serverId = r.order.id; return idb.put('drafts', d); });
    return p.then(function () {
      return idb.all('files').then(function (fs) {
        var mine = fs.filter(function (f) { return f.lid === d.lid; });
        return mine.reduce(function (pr, f) {
          return pr.then(function () {
            return uploadBlob(d.serverId, f, function (x) { renderProgress(f.fid, x); }).then(function () { return idb.del('files', f.fid); });
          });
        }, Promise.resolve());
      });
    }).then(function () {
      return api('POST', '/orders/' + d.serverId + '/save', { title: d.title, length_sec: d.length_sec, q: d.q, script: d.script, ideas: d.ideas, submit: !!d.submit });
    }).then(function () {
      return idb.del('drafts', d.lid).then(function () { if (d.submit) toast('Order "' + (d.title || 'video') + '" sent.'); });
    }).catch(function (e) {
      if (isNetErr(e)) throw e;
      d.error = e.message; d.submit = false;
      return idb.put('drafts', d);
    });
  }
  function sync() {
    if (state.syncing || !state.online || !state.token) return Promise.resolve();
    state.syncing = true;
    return idb.all('drafts').then(function (ds) {
      return ds.filter(function (d) { return d.pending; }).reduce(function (p, d) { return p.then(function () { return syncDraft(d); }); }, Promise.resolve());
    }).then(function () {
      return idb.all('outbox');
    }).then(function (items) {
      items.sort(function (a, b) { return a.created - b.created; });
      return items.reduce(function (p, it) {
        return p.then(function () {
          var call = it.type === 'action' ? api('POST', '/orders/' + it.orderId + '/' + it.action, { body: it.body })
            : it.type === 'upload' ? idb.get('files', it.fid).then(function (f) { return f ? uploadBlob(it.orderId, f).then(function () { return idb.del('files', f.fid); }) : null; })
            : Promise.resolve();
          return call.then(function () { return idb.del('outbox', it.id); }, function (e) {
            if (isNetErr(e)) throw e;
            toast(e.message, 'err');
            return idb.del('outbox', it.id);
          });
        });
      }, Promise.resolve());
    }).then(function () {
      state.syncing = false;
      return refreshLists();
    }, function () { state.syncing = false; });
  }
  // Re-draws the list only when the server data really changed (no render loop).
  function refreshLists() {
    return Promise.all([api('GET', '/orders'), idb.get('cache', 'orders')]).then(function (r) {
      if (JSON.stringify(r[0].orders) === JSON.stringify(r[1] || [])) return;
      return idb.put('cache', r[0].orders, 'orders').then(function () {
        if (/^#\/orders$|^$|^#\/?$/.test(location.hash)) vOrders(true);
      });
    }).catch(function () {});
  }
  function renderProgress(fid, x) {
    var b = document.querySelector('[data-fid="' + fid + '"] .bar > i');
    if (b) b.style.width = Math.round(x * 100) + '%';
  }

  // ---------- auth ----------
  function logoutLocal() {
    state.token = null; state.user = null;
    ls.del('token'); ls.del('user');
    document.getElementById('nav').hidden = true;
    location.hash = '#/login';
  }
  function loggedIn(r) {
    state.token = r.token; state.user = r.user;
    ls.set('token', r.token); ls.set('user', r.user);
    document.getElementById('nav').hidden = false;
    loadConfig();
    location.hash = '#/orders';
  }
  function loadConfig() {
    var p = state.token ? api('GET', '/me') : api('GET', '/config');
    return p.then(function (c) {
      state.cfg = c;
      ls.set('cfg', c);
      if (c.user) { state.user = c.user; ls.set('user', c.user); }
      document.getElementById('brand-name').textContent = c.brand;
      document.getElementById('foot-brand').textContent = c.brand;
      checkUpdates(c);
      return c;
    }).catch(function () { return state.cfg; });
  }

  // ---------- views ----------
  function view(html) {
    main.innerHTML = html;
    if (window.gsap && !reduced()) {
      window.gsap.fromTo(main, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: 'power1.inOut' });
      var st = main.querySelectorAll('.stagger > *'), rv = main.querySelectorAll('.reveal');
      if (st.length) window.gsap.from(st, { opacity: 0, y: 8, duration: 0.3, stagger: 0.03, ease: 'power1.out', clearProps: 'all' });
      if (rv.length) window.gsap.from(rv, { opacity: 0, y: 12, duration: 0.35, stagger: 0.05, ease: 'power1.out', clearProps: 'all' });
    }
  }
  function form(sel, fn) {
    var f = main.querySelector(sel);
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var btns = f.querySelectorAll('button');
      btns.forEach(function (b) { b.disabled = true; });
      Promise.resolve(fn(new FormData(f), e.submitter)).catch(function (err) {
        var n = f.querySelector('.form-err') || f.insertBefore(document.createElement('p'), f.firstChild);
        n.className = 'notice err form-err';
        n.textContent = isNetErr(err) ? 'No internet. Try again when you are online.' : err.message;
      }).then(function () { btns.forEach(function (b) { b.disabled = false; }); });
    });
  }

  function vLogin() {
    view('<section class="card narrow reveal"><h1>Log in</h1><p class="promise">' + esc(promise()) + '</p><form class="form" id="f">' +
      '<label>Email<input name="email" type="email" required autocomplete="email"></label>' +
      '<label>Password<input name="password" type="password" required autocomplete="current-password"></label>' +
      '<button class="btn primary">Log in</button></form>' +
      '<p class="muted"><a href="#/forgot">Forgot password?</a></p><p class="muted">New here? <a href="#/register">Create an account</a></p></section>');
    form('#f', function (fd) {
      return api('POST', '/login', { email: fd.get('email'), password: fd.get('password'), device: 'android' }).then(loggedIn);
    });
  }
  function vRegister() {
    view('<section class="card narrow reveal"><h1>Create your account</h1><form class="form" id="f">' +
      '<label>Your name<input name="name" required maxlength="120" autocomplete="name"></label>' +
      '<label>Email<input name="email" type="email" required autocomplete="email"></label>' +
      '<label>WhatsApp / phone <small>(optional)</small><input name="phone" maxlength="40" autocomplete="tel"></label>' +
      '<label>Currency<select name="currency">' + (((state.cfg || ls.get('cfg') || {}).currencies) || [{ code: 'PKR', label: 'PKR (Pakistani Rupee)' }, { code: 'USD', label: 'USD (US Dollar)' }]).map(function (c) { return '<option value="' + esc(c.code) + '">' + esc(c.label) + '</option>'; }).join('') + '</select></label>' +
      '<label>Password <small>(8+ characters)</small><input name="password" type="password" required minlength="8" autocomplete="new-password"></label>' +
      '<button class="btn primary">Create account</button></form><p class="muted">Have an account? <a href="#/login">Log in</a></p></section>');
    form('#f', function (fd) {
      var b = {}; fd.forEach(function (v, k) { b[k] = v; }); b.device = 'android';
      return api('POST', '/register', b).then(function (r) {
        if (r.pending) { toast(r.message); location.hash = '#/login'; return; }
        loggedIn(r);
      });
    });
  }
  function vForgot() {
    view('<section class="card narrow reveal"><h1>Forgot password</h1><p class="muted">We will email you a link to set a new password.</p>' +
      '<form class="form" id="f"><label>Email<input name="email" type="email" required></label><button class="btn primary">Send link</button></form>' +
      '<p class="muted"><a href="#/login">Back to log in</a></p></section>');
    form('#f', function (fd) {
      return api('POST', '/forgot', { email: fd.get('email') }).then(function (r) { toast(r.message); location.hash = '#/login'; });
    });
  }
  function vPrivacy() {
    var c = state.cfg || ls.get('cfg') || {};
    view('<section class="card narrow reveal"><h1>Privacy</h1><p>' + esc(c.privacy || '').replace(/\n/g, '<br>') + '</p>' +
      (c.support ? '<p class="muted">Contact: ' + esc(c.support) + '</p>' : '') + '</section>');
  }

  function brandName() { return ((state.cfg || ls.get('cfg') || {}).brand) || 'MrCopper804'; }
  function promise() { return ((state.cfg || ls.get('cfg') || {}).promise) || 'Every video is edited by hand by MrCopper804.'; }

  function statusBadge(s) {
    var names = (state.cfg && state.cfg.statuses) || {};
    return '<span class="badge s-' + esc(s) + '">' + esc(names[s] || s) + '</span>';
  }

  function vOrders(fromRefresh) {
    Promise.all([idb.get('cache', 'orders'), idb.all('drafts'), idb.all('outbox')]).then(function (r) {
      var orders = r[0] || [], drafts = r[1] || [], out = r[2] || [];
      var html = '<div class="head-row reveal"><h1>My videos</h1><a class="btn primary" href="#/new">+ New video order</a></div>';
      if (state.user && state.user.role === 'admin') {
        html += '<p class="notice reveal">You are the owner. The admin panel is on the website: <a href="' + esc(API) + '/admin">open admin panel</a>.</p>';
      }
      if (drafts.length) {
        html += '<h2 class="reveal">On this phone</h2><ul class="order-list stagger">' + drafts.map(function (d) {
          return '<li class="card order-item"><a href="#/new/' + esc(d.lid) + '"><span class="title">' + esc(d.title || 'New video') + '</span>' +
            '<span class="badge s-draft">' + (d.pending ? (d.submit ? 'Waiting to send' : 'Waiting to save') : 'Draft') + '</span>' +
            '<span class="meta">' + (d.error ? '<span class="danger">' + esc(d.error) + '</span>' : (d.pending ? 'Sends automatically when online' : 'Not sent yet')) + '</span></a></li>';
        }).join('') + '</ul>';
      }
      if (out.length) html += '<p class="muted reveal">' + out.length + ' message(s) waiting to be sent.</p>';
      if (!orders.length && !drafts.length) {
        html += '<section class="card empty reveal"><h2>No orders yet</h2><p>Start a new order: add your footage and tell us how you want it edited. ' + esc(promise()) + '</p></section>';
      } else if (orders.length) {
        html += '<ul class="order-list stagger">' + orders.map(function (o) {
          if (o.status === 'draft') return '';
          return '<li class="card order-item"><a href="#/order/' + o.id + '"><span class="title">' + esc(o.title) + '</span>' + statusBadge(o.status) +
            '<span class="meta">#' + o.id + ' · ' + o.length_sec + ' s · ' + esc(money(o.price, o.currency)) + ' · ' + esc(when(o.updated_at)) + '</span></a></li>';
        }).join('') + '</ul>';
      }
      view(html);
    });
    if (state.online && !fromRefresh) refreshLists();
  }

  // New order form: kept on the phone (works offline), sent by the sync engine.
  function vNew(lid) {
    var c = state.cfg || ls.get('cfg') || {}, u = state.user || {};
    var getD = lid ? idb.get('drafts', lid) : Promise.resolve(null);
    getD.then(function (d) {
      d = d || { lid: uid(), title: '', length_sec: '', q: {}, script: '', ideas: '', pending: false };
      if (!lid) idb.put('drafts', d);
      return idb.all('files').then(function (fs) { return [d, fs.filter(function (f) { return f.lid === d.lid; })]; });
    }).then(function (r) {
      var d = r[0], files = r[1], rate = u.rate || 0, cur = u.currency || 'PKR';
      var qs = (c.questions || []).map(function (q) {
        var v = d.q[q.key] || '';
        var input = q.type === 'select'
          ? '<select name="q.' + esc(q.key) + '"><option value="">Choose…</option>' + q.options.map(function (o) { return '<option' + (o === v ? ' selected' : '') + '>' + esc(o) + '</option>'; }).join('') + '</select>'
          : '<input name="q.' + esc(q.key) + '" type="' + (q.type === 'date' ? 'date' : 'text') + '" maxlength="' + (q.max || 200) + '" value="' + esc(v) + '">';
        return '<label>' + esc(q.label) + ' ' + (q.required ? '<span class="req">*</span>' : '<small class="opt">(optional)</small>') + input + '</label>';
      }).join('');
      view('<div class="head-row reveal"><h1>New video order</h1><span class="badge s-draft">On this phone</span></div>' +
        (d.error ? '<p class="notice err">' + esc(d.error) + '</p>' : '') +
        '<section class="card reveal"><h2>1. Your files <small class="opt">(optional)</small></h2><p class="muted">Videos, photos, logo, voice notes, script, if you have them. No files? Just describe the video below. Files stay on this phone until they are uploaded.</p>' +
        '<p class="req-note">Fields marked <span class="req">*</span> are required.</p>' +
        '<div class="drop"><input type="file" id="pick" multiple accept="video/*,image/*,audio/*,.pdf,.txt,.srt,.docx,.zip"><label for="pick" class="btn">Choose files</label></div>' +
        '<ul class="file-list" id="files">' + files.map(fileRow).join('') + '</ul></section>' +
        '<form class="form" id="f"><section class="card reveal"><h2>2. About the video</h2>' +
        '<label>Video name <span class="req">*</span><input name="title" maxlength="160" value="' + esc(d.title) + '" placeholder="e.g. Shop opening reel"></label>' +
        '<label>Length of the finished video (seconds) <span class="req">*</span><input name="length_sec" type="number" min="1" max="36000" value="' + esc(d.length_sec) + '" id="len"></label>' +
        '<p class="estimate">Price estimate: <strong id="est">' + esc(money((parseInt(d.length_sec, 10) || 0) * rate, cur)) + '</strong> <small>(' + esc(money(rate, cur)) + ' per second)</small></p>' +
        '<div class="grid2">' + qs + '</div></section>' +
        '<section class="card reveal"><h2>3. Details, script and ideas</h2><label>Script / text <small class="opt">(optional)</small><textarea name="script" rows="5" maxlength="20000">' + esc(d.script) + '</textarea></label>' +
        '<label>Tell us about the video: what it is for, what should be in it, how it should feel <span class="req">*</span><textarea name="ideas" rows="5" maxlength="10000" placeholder="What is the video about? Parts to keep or cut, colours, feeling, text on screen…">' + esc(d.ideas) + '</textarea></label></section>' +
        '<div class="actions sticky"><button class="btn danger-btn" value="delete" type="submit">Delete</button><button class="btn" value="save">Save</button><button class="btn primary" value="submit">Submit order</button></div></form>');
      var len = main.querySelector('#len'), est = main.querySelector('#est');
      len.addEventListener('input', function () { est.textContent = money((parseInt(len.value, 10) || 0) * rate, cur); });
      main.querySelector('#pick').addEventListener('change', function (e) {
        var list = main.querySelector('#files');
        Array.prototype.forEach.call(e.target.files, function (file) {
          var rec = { fid: uid(), lid: d.lid, name: file.name, size: file.size, type: file.type, blob: file, offset: 0 };
          idb.put('files', rec).then(function () {
            list.insertAdjacentHTML('beforeend', fileRow(rec));
            if (window.gsap && !reduced()) window.gsap.from(list.lastElementChild, { opacity: 0, y: 8, duration: 0.3 });
          }).catch(function () { toast('Not enough space on the phone for ' + file.name, 'err'); });
        });
        e.target.value = '';
      });
      main.querySelector('#files').addEventListener('click', function (e) {
        var b = e.target.closest('[data-remove]');
        if (!b) return;
        idb.del('files', b.dataset.remove).then(function () { b.closest('li').remove(); });
      });
      form('#f', function (fd, btn) {
        var action = btn ? btn.value : 'save';
        if (action === 'delete') {
          if (!confirm('Delete this draft and its files from the phone?')) return;
          return idb.all('files').then(function (fs) {
            return Promise.all(fs.filter(function (f) { return f.lid === d.lid; }).map(function (f) { return idb.del('files', f.fid); }));
          }).then(function () { return idb.del('drafts', d.lid); }).then(function () { location.hash = '#/orders'; });
        }
        d.title = fd.get('title'); d.length_sec = fd.get('length_sec'); d.script = fd.get('script'); d.ideas = fd.get('ideas'); d.q = {};
        (c.questions || []).forEach(function (q) { d.q[q.key] = fd.get('q.' + q.key) || ''; });
        d.error = null;
        if (action === 'submit') {
          var missing = (c.questions || []).filter(function (q) { return q.required && !d.q[q.key]; }).map(function (q) { return q.label; });
          if (!d.title) missing.unshift('Video name');
          if (!(parseInt(d.length_sec, 10) > 0)) missing.push('Length in seconds');
          // Files, voice and script are optional; the details are required (owner, 2026-10-29).
          if ((d.ideas || '').trim().length < 10) missing.push('Details about the video (at least a sentence)');
          return Promise.resolve().then(function () {
            if (missing.length) throw new Error('Please fill in: ' + missing.join(', '));
            d.pending = true; d.submit = true;
            return idb.put('drafts', d).then(function () {
              toast(state.online ? 'Sending your order…' : 'Saved. It will be sent when you are online.');
              location.hash = '#/orders';
              sync();
            });
          });
        }
        d.pending = false;
        return idb.put('drafts', d).then(function () { toast('Draft saved on this phone.'); });
      });
    });
  }
  function fileRow(f) {
    return '<li data-fid="' + esc(f.fid) + '"><span class="fname">' + esc(f.name) + '</span><span class="muted">' + bytes(f.size) + '</span>' +
      '<button class="link danger" type="button" data-remove="' + esc(f.fid) + '">Remove</button><span class="bar"><i></i></span></li>';
  }

  function vOrder(id) {
    var cached = idb.get('cache', 'order:' + id);
    var fresh = state.online ? api('GET', '/orders/' + id).then(function (r) { idb.put('cache', r.order, 'order:' + id); return r.order; }).catch(function () { return null; }) : Promise.resolve(null);
    Promise.all([cached, fresh, idb.all('outbox')]).then(function (r) {
      var o = r[1] || r[0];
      if (!o) { view('<section class="card reveal"><h2>Not available offline</h2><p>Open this order once while online to keep it on the phone.</p></section>'); return; }
      var waiting = r[2].filter(function (x) { return String(x.orderId) === String(id); });
      var steps = [['submitted', 'Received'], ['in_progress', 'Editing'], ['delivered', 'Ready'], ['approved', 'Approved']];
      var reach = { submitted: 0, in_progress: 1, revision: 1, delivered: 2, approved: 3 }[o.status] || 0;
      var v = o.versions[0];
      var html = '<div class="head-row reveal"><h1>' + esc(o.title) + '</h1>' + statusBadge(o.status) + '</div>' +
        (!r[1] ? '<p class="muted reveal">Showing the copy saved on this phone.</p>' : '') +
        '<ol class="progress reveal">' + steps.map(function (s, i) { return '<li class="' + (i <= reach ? 'done' : '') + '">' + s[1] + '</li>'; }).join('') + '</ol>';
      if (v) {
        html += '<section class="card reveal"><h2>Version ' + v.number + '</h2>' +
          (/^video\//.test(v.mime) ? '<video class="player" controls playsinline preload="metadata" id="player"></video>' : /^image\//.test(v.mime) ? '<img class="player" id="player" alt="">' : '') +
          (v.note ? '<p>' + esc(v.note).replace(/\n/g, '<br>') + '</p>' : '') +
          '<p class="row-left"><button class="btn" id="save-off" type="button">Save for offline</button> <span class="muted" id="off-state"></span></p>';
        if (o.status === 'delivered') {
          html += '<div class="review"><h3>Koi changes chahiye? Do you want any changes?</h3>' +
            '<form class="form" id="fc"><textarea name="body" rows="4" required minlength="3" maxlength="10000" placeholder="Example: at 0:12 make the text bigger, use a happier song…"></textarea><button class="btn">Send changes</button></form>' +
            '<form class="form" id="fa"><button class="btn primary">It\'s perfect, approve</button></form></div>';
        } else if (o.status === 'revision') {
          html += '<p class="notice">We got your changes. ' + esc(brandName()) + ' is working on the next version.</p>';
        }
        html += '</section>';
      } else {
        html += '<section class="card reveal"><h2>We are on it</h2><p>Your order was received. ' + esc(promise()) + ' The finished video will appear here.</p></section>';
      }
      if (waiting.length) html += '<p class="notice reveal">' + waiting.length + ' message(s) will be sent when you are online.</p>';
      html += '<section class="card reveal"><h2>Messages</h2><ul class="thread">' + o.messages.map(function (m) {
        return '<li class="msg ' + (m.from === 'me' ? 'me' : 'them') + '"><span class="who">' + (m.from === 'me' ? 'You' : esc((state.cfg && state.cfg.brand) || 'Studio')) + ' · ' + esc(when(m.created_at)) + '</span>' + esc(m.body).replace(/\n/g, '<br>') + '</li>';
      }).join('') + '</ul>' + (o.status !== 'approved' ? '<form class="form inline" id="fm"><textarea name="body" rows="2" required maxlength="10000" placeholder="Write a message…"></textarea><button class="btn">Send</button></form>' : '') + '</section>';
      if (o.versions.length > 1) {
        html += '<section class="card reveal"><h2>Earlier versions</h2><ul class="file-list">' + o.versions.slice(1).map(function (x) {
          return '<li><span class="fname">Version ' + x.number + ' · ' + esc(when(x.created_at)) + '</span><a href="' + esc(x.url) + '" target="_blank" rel="noopener">Watch</a></li>';
        }).join('') + '</ul></section>';
      }
      if (o.status !== 'approved') {
        html += '<section class="card reveal"><h2>Add more files</h2><div class="drop"><input type="file" id="pick2" multiple accept="video/*,image/*,audio/*,.pdf,.txt,.srt,.docx,.zip"><label for="pick2" class="btn">Choose files</label></div><ul class="file-list" id="files2"></ul></section>';
      }
      html += '<details class="card reveal"><summary>Your order details</summary><dl class="details"><dt>Length</dt><dd>' + o.length_sec + ' seconds</dd>' +
        '<dt>Price</dt><dd>' + esc(money(o.price, o.currency)) + (o.price_is_final ? '' : ' (estimate)') + '</dd>' +
        ((state.cfg && state.cfg.questions) || []).filter(function (q) { return o.answers[q.key]; }).map(function (q) { return '<dt>' + esc(q.label) + '</dt><dd>' + esc(o.answers[q.key]) + '</dd>'; }).join('') +
        (o.ideas ? '<dt>Ideas</dt><dd>' + esc(o.ideas).replace(/\n/g, '<br>') + '</dd>' : '') +
        '<dt>Files</dt><dd>' + o.files.filter(function (f) { return f.kind === 'input'; }).map(function (f) { return esc(f.name) + ' (' + bytes(f.size) + ')'; }).join('<br>') + '</dd></dl></details>';
      view(html);
      if (v) {
        var pl = main.querySelector('#player'), st = main.querySelector('#off-state'), btn = main.querySelector('#save-off');
        idb.get('videos', 'v' + v.id).then(function (blob) {
          if (pl) pl.src = blob ? URL.createObjectURL(blob) : v.url;
          if (blob) { st.textContent = 'Saved on this phone (' + bytes(blob.size) + ')'; btn.hidden = true; }
          if (pl && window.gsap && !reduced()) window.gsap.fromTo(pl, { boxShadow: '0 0 0 0 rgba(255,46,147,0)' }, { boxShadow: '0 0 0 6px rgba(255,46,147,.35)', duration: 0.5, yoyo: true, repeat: 1, delay: 0.4 });
        });
        btn.addEventListener('click', function () {
          if (!state.online) { toast('Connect to the internet to save the video.', 'err'); return; }
          btn.disabled = true; st.textContent = 'Downloading…';
          fetch(v.url).then(function (r) { if (!r.ok) throw new Error('Download failed'); return r.blob(); })
            .then(function (b) { return idb.put('videos', b, 'v' + v.id).then(function () { st.textContent = 'Saved on this phone (' + bytes(b.size) + ')'; btn.hidden = true; }); })
            .catch(function (e) { st.textContent = e.message; btn.disabled = false; });
        });
      }
      function act(sel, action, confirmMsg) {
        var f = main.querySelector(sel);
        if (!f) return;
        form(sel, function (fd) {
          if (confirmMsg && !confirm(confirmMsg)) return;
          var body = fd.get('body') || '';
          return outboxAdd({ type: 'action', orderId: id, action: action, body: body }).then(function () {
            toast(state.online ? 'Sent.' : 'Saved. It will be sent when you are online.');
            setTimeout(function () { vOrder(id); }, state.online ? 700 : 0);
          });
        });
      }
      act('#fc', 'changes');
      act('#fa', 'approve', 'Approve this version as final?');
      act('#fm', 'message');
      var p2 = main.querySelector('#pick2');
      if (p2) p2.addEventListener('change', function (e) {
        var list = main.querySelector('#files2');
        Array.prototype.forEach.call(e.target.files, function (file) {
          var rec = { fid: uid(), lid: null, name: file.name, size: file.size, type: file.type, blob: file, offset: 0 };
          idb.put('files', rec).then(function () {
            list.insertAdjacentHTML('beforeend', fileRow(rec));
            return outboxAdd({ type: 'upload', orderId: id, fid: rec.fid });
          });
        });
        e.target.value = '';
      });
    });
  }

  function vAccount() {
    var u = state.user || {};
    var info = CAP.App ? CAP.App.getInfo() : Promise.resolve({ version: 'web', build: '0' });
    info.then(function (i) {
      view('<section class="card narrow reveal"><h1>Account</h1><p><strong>' + esc(u.name) + '</strong><br>' + esc(u.email) + '</p>' +
        '<p class="muted">Rate: ' + esc(money(u.rate, u.currency)) + ' per second of finished video</p>' +
        '<h2>Change password</h2><form class="form" id="f"><label>Current password<input name="current" type="password" required></label>' +
        '<label>New password (8+ characters)<input name="new" type="password" required minlength="8"></label><button class="btn">Change password</button></form>' +
        '<h2>App</h2><p class="muted">App ' + esc(i.version) + ' (' + esc(i.build) + ') · screens ' + esc(BUNDLE) + '</p>' +
        '<p><button class="btn" id="upd" type="button">Check for updates</button></p>' +
        '<p><button class="btn" id="clear" type="button">Remove saved videos from this phone</button></p>' +
        '<p><button class="btn danger-btn" id="out" type="button">Log out</button></p></section>');
      form('#f', function (fd) {
        return api('POST', '/password', { current: fd.get('current'), new: fd.get('new') }).then(function (r) {
          state.token = r.token; ls.set('token', r.token); toast('Password changed. Other devices were logged out.');
        });
      });
      main.querySelector('#upd').addEventListener('click', function () { loadConfig().then(function () { toast('You have the latest version.'); }); });
      main.querySelector('#clear').addEventListener('click', function () { idb.clear('videos').then(function () { toast('Saved videos removed.'); }); });
      main.querySelector('#out').addEventListener('click', function () {
        api('POST', '/logout', {}).catch(function () {}).then(function () { idb.clear('cache'); logoutLocal(); });
      });
    });
  }

  // ---------- updates ----------
  // 1) Live update: new screens downloaded from our own server.
  // 2) Native update: a new APK only for native changes (icon, plugins): show an Update bar.
  function verNum(v) { return String(v || '0.0.0').split('.').map(function (x) { return parseInt(x, 10) || 0; }).reduce(function (a, b) { return a * 1000 + b; }, 0); }
  function checkUpdates(c) {
    if (!c || !c.app) return;
    var a = c.app, U = CAP.CapacitorUpdater;
    var info = CAP.App ? CAP.App.getInfo() : Promise.resolve({ build: String((window.APP_NATIVE_BUILD || 0)) });
    info.then(function (i) {
      var build = parseInt(i.build, 10) || 0;
      if (a.native_version > build && a.apk_url) showUpdateBar('New app version', a.notes, a.apk_url);
      if (U && a.bundle_url && a.bundle_version && verNum(a.bundle_version) > verNum(BUNDLE) && build >= (a.bundle_min_native || 0) && !ls.get('bundleTried:' + a.bundle_version)) {
        ls.set('bundleTried:' + a.bundle_version, 1);
        U.download({ url: a.bundle_url, version: a.bundle_version, checksum: a.bundle_sha256 || undefined }).then(function (b) {
          return U.next({ id: b.id });
        }).then(function () { toast('New screens downloaded. They load next time you open the app.'); }).catch(function () {});
      }
    });
  }
  function showUpdateBar(title, notes, url) {
    if (document.querySelector('.update-bar')) return;
    var bar = document.createElement('div');
    bar.className = 'update-bar';
    bar.innerHTML = '<span><strong></strong> <small></small></span><a class="btn primary" target="_blank" rel="noopener">Update</a><button class="link" type="button">Later</button>';
    bar.querySelector('strong').textContent = title;
    bar.querySelector('small').textContent = notes || '';
    bar.querySelector('a').href = url;
    bar.querySelector('button').addEventListener('click', function () { bar.remove(); });
    document.body.appendChild(bar);
  }

  // ---------- splash: every launch ----------
  function splash() {
    var el = document.getElementById('splash');
    document.getElementById('splash-host').textContent = API.replace(/^https?:\/\//, '');
    var g = window.gsap;
    if (!g || reduced() || window.APP_SKIP_SPLASH) { el.remove(); return; }
    var word = el.querySelector('.splash-word');
    var brand = (state.cfg && state.cfg.brand) || 'MrCopper804';
    word.innerHTML = brand.split('').map(function (ch) { return ch === ' ' ? '<span>&nbsp;</span>' : '<span>' + esc(ch) + '</span>'; }).join('');
    var circle = el.querySelector('circle'), len = 2 * Math.PI * 75.5;
    g.set(circle, { strokeDasharray: len, strokeDashoffset: len });
    var tl = g.timeline({ onComplete: function () { el.remove(); } });
    tl.to(circle, { strokeDashoffset: 0, duration: 0.9, ease: 'power2.inOut' }, 0)
      .fromTo('.splash-mark', { scale: 0.6, rotation: -14, opacity: 0, filter: 'blur(8px)' }, { scale: 1.04, rotation: 0, opacity: 1, filter: 'blur(0px)', duration: 0.55, ease: 'power3.out' }, 0.25)
      .to('.splash-mark', { scale: 1, duration: 0.16, ease: 'power1.out' }, 0.8)
      .from('.splash-word span', { y: 14, opacity: 0, duration: 0.4, stagger: 0.06, ease: 'power2.out' }, 0.8)
      .from('.splash-sub', { opacity: 0, letterSpacing: '1.2em', duration: 0.5, ease: 'power2.out' }, 1.25)
      .from('.splash-host', { opacity: 0, y: 8, duration: 0.35, ease: 'power1.out' }, 1.45)
      .fromTo('.splash-ring', { filter: 'drop-shadow(0 0 0 rgba(0,212,184,0))' }, { filter: 'drop-shadow(0 0 14px rgba(245,166,35,.8))', duration: 0.3, yoyo: true, repeat: 1 }, 1.2)
      .to(el, { opacity: 0, scale: 1.04, duration: 0.3, ease: 'power1.in' }, '+=0.7');
    el.addEventListener('click', function () { tl.progress(1); });
  }

  // ---------- router ----------
  function route() {
    var h = location.hash || '#/orders', m;
    var open = ['#/login', '#/register', '#/forgot', '#/privacy'];
    if (!state.token && open.indexOf(h) < 0) { location.hash = '#/login'; return; }
    if (state.token && open.slice(0, 3).indexOf(h) >= 0) { location.hash = '#/orders'; return; }
    if (h === '#/login') return vLogin();
    if (h === '#/register') return vRegister();
    if (h === '#/forgot') return vForgot();
    if (h === '#/privacy') return vPrivacy();
    if (h === '#/account') return vAccount();
    if (h === '#/new') return vNew(null);
    if ((m = h.match(/^#\/new\/(L[a-z0-9]+)$/))) return vNew(m[1]);
    if ((m = h.match(/^#\/order\/(\d+)$/))) return vOrder(m[1]);
    return vOrders();
  }
  window.addEventListener('hashchange', route);

  // ---------- start ----------
  document.addEventListener('DOMContentLoaded', function () {
    state.token = ls.get('token');
    state.user = ls.get('user');
    state.cfg = ls.get('cfg');
    document.getElementById('app-ver').textContent = 'v' + BUNDLE;
    if (state.token) document.getElementById('nav').hidden = false;
    if (CAP.CapacitorUpdater) CAP.CapacitorUpdater.notifyAppReady().catch(function () {});
    setOnline(navigator.onLine);
    window.addEventListener('load', splash);
    route();
    loadConfig();
    if (CAP.App) CAP.App.addListener('resume', function () { sync(); loadConfig(); });
    setInterval(function () { if (state.online) sync(); }, 30000);
  });
})();
