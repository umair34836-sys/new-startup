// Screen recorder for tutorials: drives a real page with Playwright, draws a visible mouse cursor that moves to
// each target and plays a press + ripple animation on every click, and records the page with the CDP screencast
// (sharp JPEG frames, much cleaner than Playwright's recordVideo). Writes <out>/frames/*.jpg, <out>/events.json
// (every click/fake-click/mark with its time in seconds from the first frame, for click sounds and captions) and
// encodes <out>/recording.mp4 at a constant 30 fps.
//
//   const { Recorder } = require('/home/user/new-startup/library/tools/screen_recorder.js');
//   const rec = await Recorder.launch({ out: '/path/run1', width: 1920, height: 1080, zoom: 1.4, block: [/doubleclick/] });
//   (zoom 1.4 = CSS zoom on <html>: the page lays out like a ~1370 px wide window but renders natively at 1920x1080,
//    so UI text is big AND sharp. deviceScaleFactor does not help: the CDP screencast sends DIP-sized frames.)
//   await rec.goto('https://example.com');
//   await rec.click('text=More information');          // real click, cursor + ripple
//   await rec.type('#q', 'hello');                      // click into the field, then type at human speed
//   await rec.select('#edition', 'Java');               // <select>: click + choose (native popups don't render)
//   await rec.fakeClick('button[type=submit]');         // cursor + ripple only, NO real click (don't submit live forms)
//   await rec.mark('step2');                            // timestamp for captions/VO
//   await rec.finish();                                 // stops, writes events.json, encodes recording.mp4
// Run with NODE_PATH="$(npm root -g)" so require('playwright') resolves.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { chromium } = require('playwright');

const CURSOR_JS = `(() => {
  if (window.__recCursor) return;
  const install = () => {
    if (!document.body || document.getElementById('__rec_cursor')) return;
    const st = document.createElement('style');
    st.textContent = \`
      #__rec_cursor{position:fixed;left:0;top:0;width:34px;height:34px;z-index:2147483647;pointer-events:none;
        transform:translate(-200px,-200px);transition:none;filter:drop-shadow(0 3px 4px rgba(0,0,0,.55))}
      #__rec_cursor svg{width:34px;height:34px;transform-origin:4px 3px;transition:transform .09s ease-out}
      #__rec_cursor.down svg{transform:scale(.82)}
      .__rec_ripple{position:fixed;z-index:2147483646;pointer-events:none;width:22px;height:22px;margin:-11px 0 0 -11px;
        border-radius:50%;border:4px solid #ffb22e;background:rgba(255,178,46,.28);animation:__rec_rip .55s ease-out forwards}
      @keyframes __rec_rip{0%{transform:scale(.4);opacity:1}100%{transform:scale(3.4);opacity:0}}\`;
    document.head.appendChild(st);
    const c = document.createElement('div');
    c.id = '__rec_cursor';
    c.innerHTML = '<svg viewBox="0 0 24 24"><path d="M4 2.5 L4 19.5 L8.6 15.4 L11.6 22 L14.6 20.7 L11.7 14.2 L18 14.2 Z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>';
    document.body.appendChild(c);
    const p = window.__recPos || { x: -200, y: -200 };
    c.style.transform = 'translate(' + (p.x / Z() - 4) + 'px,' + (p.y / Z() - 3) + 'px)';
  };
  // Event/viewport pixels -> CSS px inside a zoomed <html> (fixed elements get multiplied by the zoom).
  const Z = () => parseFloat(getComputedStyle(document.documentElement).zoom) || 1;
  window.__recCursor = {
    move(x, y) { window.__recPos = { x, y }; x /= Z(); y /= Z(); const c = document.getElementById('__rec_cursor');
      if (c) c.style.transform = 'translate(' + (x - 4) + 'px,' + (y - 3) + 'px)'; },
    press(x, y) { x /= Z(); y /= Z(); const c = document.getElementById('__rec_cursor'); if (c) { c.classList.add('down');
      setTimeout(() => c.classList.remove('down'), 160); }
      const r = document.createElement('div'); r.className = '__rec_ripple'; r.style.left = x + 'px'; r.style.top = y + 'px';
      document.body.appendChild(r); setTimeout(() => r.remove(), 700); }
  };
  document.addEventListener('mousemove', e => window.__recCursor.move(e.clientX, e.clientY), true);
  document.addEventListener('mousedown', e => window.__recCursor.press(e.clientX, e.clientY), true);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', install); else install();
  new MutationObserver(install).observe(document.documentElement, { childList: true, subtree: true });
})();`;

const sleep = ms => new Promise(r => setTimeout(r, ms));
const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

class Recorder {
  static async launch({ out, width = 1920, height = 1080, zoom = 1, block = [], quality = 92 }) {
    const r = new Recorder();
    r.out = out; r.w = width; r.h = height; r.quality = quality;
    fs.mkdirSync(path.join(out, 'frames'), { recursive: true });
    r.browser = await chromium.launch();
    r.ctx = await r.browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1 });
    if (block.length) await r.ctx.route('**/*', route => (block.some(b => b.test(route.request().url())) ? route.abort() : route.continue()));
    if (zoom !== 1) await r.ctx.addInitScript(`document.addEventListener('DOMContentLoaded', () => { document.documentElement.style.zoom = '${zoom}'; });`);
    await r.ctx.addInitScript(CURSOR_JS);
    r.page = await r.ctx.newPage();
    r.pos = { x: width * 0.62, y: height * 0.55 };
    r.frames = []; r.events = []; r.t0 = null;
    return r;
  }

  async startCapture() {
    this.cdp = await this.ctx.newCDPSession(this.page);
    this.cdp.on('Page.screencastFrame', async f => {
      const ts = f.metadata.timestamp;
      if (this.t0 === null) this.t0 = ts;
      const file = path.join(this.out, 'frames', String(this.frames.length).padStart(6, '0') + '.jpg');
      fs.writeFileSync(file, Buffer.from(f.data, 'base64'));
      this.frames.push({ file, t: ts - this.t0 });
      try { await this.cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }); } catch (_) {}
    });
    await this.cdp.send('Page.startScreencast', { format: 'jpeg', quality: this.quality, maxWidth: this.w, maxHeight: this.h, everyNthFrame: 1 });
    while (this.t0 === null) await sleep(20);
  }

  now() { return this.t0 === null ? 0 : Date.now() / 1000 - this.t0; }
  // x/y in events are video pixels.
  log(type, extra = {}) {
    const e = { type, t: +this.now().toFixed(3), ...extra }; this.events.push(e); return e;
  }

  async goto(url, { wait = 1500 } = {}) {
    await this.page.goto(url, { waitUntil: 'networkidle', timeout: 90000 }).catch(() => {});
    await this.page.evaluate(([x, y]) => window.__recCursor && window.__recCursor.move(x, y), [this.pos.x, this.pos.y]);
    if (!this.cdp) await this.startCapture();
    this.log('goto', { url });
    await sleep(wait);
  }

  // Element box in viewport pixels; smooth-scrolls it to the middle first when it sits outside the comfortable band
  // (the top ~160 px are often a fixed header); scrollIntoView also scrolls inside modals.
  async box(sel) {
    const loc = this.page.locator(sel).first();
    let b = await loc.boundingBox();
    if (b && (b.y < 160 || b.y + b.height > this.h - 100)) {
      await loc.evaluate(el => el.scrollIntoView({ block: 'center', behavior: 'smooth' }));
      this.log('scroll', { sel });
      await sleep(900);
      b = await loc.boundingBox();
    }
    if (!b) throw new Error('not visible: ' + sel);
    return b;
  }

  // Eased glide of the real mouse (the drawn cursor follows mousemove events).
  async moveTo(x, y, ms = 650) {
    const from = { ...this.pos }; const n = Math.max(6, Math.round(ms / 40)); const t0 = Date.now();
    for (let i = 1; i <= n; i++) {
      const k = ease(i / n);
      await this.page.mouse.move(from.x + (x - from.x) * k, from.y + (y - from.y) * k);
      const lag = t0 + (ms * i) / n - Date.now();
      if (lag > 0) await sleep(lag);
    }
    this.pos = { x, y };
  }

  async target(sel, fx = 0.5, fy = 0.5) {
    const b = await this.box(sel);
    return { x: Math.round(b.x + b.width * fx), y: Math.round(b.y + b.height * fy), box: b };
  }

  async click(sel, { fx = 0.5, fy = 0.5, label, after = 700 } = {}) {
    const p = await this.target(sel, fx, fy);
    await this.moveTo(p.x, p.y); await sleep(180);
    this.log('click', { sel, label, x: p.x, y: p.y });
    await this.page.mouse.down(); await sleep(90); await this.page.mouse.up();
    await sleep(after);
  }

  // Cursor + press + ripple at the target WITHOUT clicking it (e.g. a live "Submit" that must not be sent).
  async fakeClick(sel, { fx = 0.5, fy = 0.5, label, after = 900 } = {}) {
    const p = await this.target(sel, fx, fy);
    await this.moveTo(p.x, p.y); await sleep(220);
    this.log('fakeclick', { sel, label, x: p.x, y: p.y });
    await this.page.evaluate(([x, y]) => window.__recCursor.press(x, y), [p.x, p.y]);
    await sleep(after);
  }

  async type(sel, text, { delay = 55, label, after = 500, fx = 0.3 } = {}) {
    await this.click(sel, { fx, label, after: 250 });
    this.log('type', { sel, text });
    await this.page.keyboard.type(text, { delay });
    await sleep(after);
  }

  async select(sel, value, { label, after = 700 } = {}) {
    await this.click(sel, { fx: 0.5, label, after: 250 });
    await this.page.selectOption(sel, value).catch(async () => this.page.selectOption(sel, { label: value }));
    this.log('select', { sel, value });
    await sleep(after);
  }

  async scrollTo(sel, { block = 'start', offset = 0, after = 900 } = {}) {
    await this.page.evaluate(([s, blk, off]) => {
      const el = document.querySelector(s); if (!el) return;
      const y = el.getBoundingClientRect().top + window.scrollY - off - (blk === 'center' ? innerHeight / 2 : 0);
      window.scrollTo({ top: y, behavior: 'smooth' });
    }, [sel, block, offset]);
    this.log('scroll', { sel });
    await sleep(after);
  }

  async mark(name) { this.log('mark', { name }); }
  async wait(ms) { await sleep(ms); }

  async finish({ fps = 30 } = {}) {
    const end = this.now();
    await this.cdp.send('Page.stopScreencast').catch(() => {});
    await sleep(300);
    await this.browser.close();
    const fr = this.frames.sort((a, b) => a.t - b.t);
    // concat list: each frame lasts until the next one; the last one until the end time.
    let list = '';
    fr.forEach((f, i) => {
      const d = (i + 1 < fr.length ? fr[i + 1].t : end) - f.t;
      list += `file '${f.file}'\nduration ${Math.max(d, 0.001).toFixed(4)}\n`;
    });
    list += `file '${fr[fr.length - 1].file}'\n`;
    const listFile = path.join(this.out, 'frames.txt');
    fs.writeFileSync(listFile, list);
    fs.writeFileSync(path.join(this.out, 'events.json'), JSON.stringify({ duration: +end.toFixed(3), width: this.w, height: this.h, frames: fr.length, events: this.events }, null, 1));
    const mp4 = path.join(this.out, 'recording.mp4');
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', listFile,
      '-vf', `fps=${fps},scale=${this.w}:${this.h}:flags=lanczos,format=yuv420p`, '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', mp4]);
    return { mp4, duration: end, frames: fr.length };
  }
}

module.exports = { Recorder };
